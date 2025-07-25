<template>
  <div class="content-box Facial-Secondary-Review-box">
    <div class="contentbodybox-top">
      <div class="contentbodybox-top-l">
        <el-date-picker
          v-model="filterData.time"
          type="daterange"
          range-separator="-"
          start-placeholder="Start Time"
          end-placeholder="End Time"
        />
        <el-select
          placeholder="Status"
          style="width: 240px"
          v-model="filterData.status"
        >
          <el-option
            v-for="item in option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>

        <el-button @click="search">Search</el-button>
      </div>
      <div class="contentbodybox-top-r">
        <el-checkbox
          label="Check All"
          size="large"
          v-model="checkAll"
          :indeterminate="isIndeterminate"
          @change="CheckAllChange"
        />
        <el-button type="primary" @click="operateAll('nofake')"
          >No Fake</el-button
        >
        <el-button type="danger" @click="operateAll('fake')">Fake</el-button>
      </div>
    </div>
    <div class="facebox" v-loading="loading">
      <ul class="imglist" v-if="list.length > 0">
        <li v-for="(item, index) in list" :key="item.NIK" class="infoBox">
          <el-checkbox
            v-if="item.status != 'no_fake'"
            v-model="item.checkStatus"
            size="large"
          />
          <div v-else style="height: 20px"></div>
          <div class="infoTextBox">
            <div class="info-l">
              <span>CreateTime</span>
              <span>NIK</span>  
              <span>Status</span>
              <span>Reason</span>
            </div>
            <div class="info-r">
              <span>{{ item.create_time }}</span>
              <span>{{ item.nik }}</span>
              <span :class="item.status">{{ item.status }}</span>
              <span  class="reason">{{ item.reason }}</span>
            </div>
          </div>
          <div class="imgBox">
            <img
              alt=""
              v-if="item.image_url == ''"
              src="../../../public/头像.png"
            />
            <img
              alt=""
              v-else
              :src="item.image_url"
              @click="openPreview(index)"
            />
          </div>
          <div class="buttonBox" v-if="item.status != 'no_fake'">
            <el-button
              type="primary"
              plain
              size="small"
              @click="OpenAlert(item, 'no_fake')"
              >No Fake</el-button
            >
            <el-button
              type="danger"
              plain
              size="small"
               v-if="item.status != 'is_fake'"
              @click="OpenAlert(item, 'is_fake')"
              >Fake</el-button
            >
          </div>
        </li>
      </ul>

      <el-empty :image-size="200" v-else />
    </div>
    <div class="Pagination-box">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        v-model:current-page="currentPage"
        :page-sizes="[20, 30, 40,50]"
        :page-size="pagesize"
        layout="sizes, prev, pager, next"
        :total="total"
      >
      </el-pagination>
    </div>
    <el-dialog v-model="AlertStatus" title="Tips" width="400">
      <span v-if="OperatType == 'no_fake'"
        >Are you sure it's not a fake card?</span
      >
      <span v-else>Are you sure it's fake card?</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button size="small" @click="AlertStatus = false">No</el-button>
          <el-button
            size="small"
            type="primary"
            :loading="buttonLoad"
            @click="Operation"
          >
            Yes
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>
  
  <script>
import { getfakeIdcard, faceOperation } from "@/api/api.js";
export default {
  data() {
    return {
      currentIndex: 0,
      filterData: {
        time: [],
        status: "pending",
      },
      list: [],
      //分页，
      currentPage: 1,
      pagesize: 20,
      total: 0,
      loading: false,
      option: [
        { value: "pending", label: "Pending" },
        { value: "is_fake", label: "Fake" },
        { value: "no_fake", label: "No Fake" },
      ],
      AlertStatus: false,
      OperatType: "",
      DelAlertStatus: false,
      buttonLoad: false,
      AlertDataArr: {}, //用于弹窗后的确定传参
      checkAll: false,
      isIndeterminate: false,
    };
  },
  watch: {
    list: {
      handler(newList) {
        // 拥有 checkStatus 属性的项数量
        const totalWithCheckStatus = newList.filter(
          (item) => "checkStatus" in item
        ).length;
        // checkStatus 为 true 的项数量
        const checkedCount = newList.filter(
          (item) => item.checkStatus === true
        ).length;
        // 判断 isIndeterminate 的状态
        if (totalWithCheckStatus === 0 || checkedCount === 0) {
          // 如果没有 checkStatus 属性，或者所有 checkStatus 为 false
          this.isIndeterminate = false;
        } else {
          // 其他情况下，判断是否部分选中
          this.isIndeterminate = checkedCount !== totalWithCheckStatus;
        }
      },
      deep: true, // 深度监听，确保能够监听到对象内部的变化
    },
  },
  methods: {
    openPreview(index) {
      let urlList = this.list.map((item, index) => {
        return item.image_url; // 添加唯一标识
      });
      this.$hevueImgPreview({
        multiple: true,
        nowImgIndex: index,
        imgList: urlList,
        dataList: this.list,
        onupload: (data) => {
          this.OpenAlert(data.dataUrl, "no_fake");
        },
        ondelete: (data) => {
          this.OpenAlert(data.dataUrl, "is_fake");
        },
        type: "fake",
      });
    },

    closePreview() {
      this.$store.commit("SET_VISIBLE", false);
    },
    // 多选操作
    operateAll(type) {
      let filterArr = this.list.filter((item) => item.checkStatus === true);
      if (type == "fake") {
        this.OpenAlert(filterArr, "is_fake");
      } else {
        this.OpenAlert(filterArr, "no_fake");
      }
    },
    // 多选按钮
    CheckAllChange(val) {
      this.list.forEach((item) => {
        if ("checkStatus" in item) {
          // 判断是否有 checkStatus 属性
          item.checkStatus = val ? true : false; // 根据 val 设置 checkStatus 的值
        }
      });
    },
    // 打开弹窗
    OpenAlert(data, OperatType) {
      if (Array.isArray(data)) {
        this.AlertDataArr = data; // 如果是数组，直接赋值
      } else {
        this.AlertDataArr = [data]; // 如果不是数组，将其包装成数组
      }
      this.AlertStatus = true;
      this.OperatType = OperatType;
    },

    Operation() {
      let arr = this.AlertDataArr.map((item) => {
        return {
          image_id: item.image_id,
          operation: this.OperatType,
        };
      });
      faceOperation({
        bacth_list: arr,
      })
        .then((res) => {
          if (res.re_code == 200) {
            this.$message.success(res.msg);
            // 遍历 arr，逐个删除 this.list 中对应的项
            arr.forEach((item) => {
              const index = this.list.findIndex(
                (listItem) => listItem.image_id === item.image_id
              );
              if (index !== -1) {
                this.list.splice(index, 1);
              }
            });

            this.AlertStatus = false;
            this.buttonLoad = false;
            this.closePreview();
          }
        })
        .catch((err) => {
          console.error("上传出错：", err);
          this.$message.error("上传出错，请稍后重试！");
          this.buttonLoad = false;
        });
    },

    handleCurrentChange(val) {
      this.currentPage = val;
      this.getDataList({
        page: this.currentPage,
        page_size: this.pagesize,
        start_time: this.formatDate(this.filterData.time?.[0]),
        end_time: this.formatDate(this.filterData.time?.[1]),
        status: this.filterData.status,
      });
    },
    // 页数
    handleSizeChange(val) {
      this.currentPage = 1;
      this.pagesize = val;
      this.getDataList({
        page: this.currentPage,
        page_size: this.pagesize,
        start_time: this.formatDate(this.filterData.time?.[0]),
        end_time: this.formatDate(this.filterData.time?.[1]),
        status: this.filterData.status,
      });
    },
    formatDate(dateString) {
      if (!dateString) {
        return undefined; // 如果 dateString 为 false，返回 undefined
      }
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    },
    getFirstThreeDays() {
      const today = new Date();
      // 获取今天的日期
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, "0");
      const day = String(today.getDate()).padStart(2, "0");
      const todayString = `${year}-${month}-${day}`;

      // 获取前三天的日期
      const threeDaysAgo = new Date();
      threeDaysAgo.setDate(today.getDate() - 3); // 设置为前三天
      const threeDaysAgoYear = threeDaysAgo.getFullYear();
      const threeDaysAgoMonth = String(threeDaysAgo.getMonth() + 1).padStart(
        2,
        "0"
      );
      const threeDaysAgoDay = String(threeDaysAgo.getDate()).padStart(2, "0");
      const threeDaysAgoString = `${threeDaysAgoYear}-${threeDaysAgoMonth}-${threeDaysAgoDay}`;

      return [threeDaysAgoString, todayString]; // 返回 [前三天时间, 今天时间]
    },
    search() {
      this.currentPage = 1;
      this.getDataList({
        page: this.currentPage,
        page_size: this.pagesize,
        start_time: this.formatDate(this.filterData.time?.[0]),
        end_time: this.formatDate(this.filterData.time?.[1]),
        status: this.filterData.status,
      });
    },
    async getDataList(obj) {
      this.loading = true;
      let res = await getfakeIdcard(obj);
      if (res.re_code == 200) {
        this.isIndeterminate = false;
        this.checkAll = false;
        this.list = res.msg.data.map((item) => {
          return item.status === "no_fake"
            ? item
            : {
                ...item, // 保留原有属性
                checkStatus: false, // 新增 checkStatus 属性
              };
        });

        this.total = res.msg.total;
      }
      this.loading = false;
    },
  },
  mounted() {
    this.filterData.time = this.getFirstThreeDays();
    this.getDataList({
      page: this.currentPage,
      page_size: this.pagesize,
      start_time: this.formatDate(this.filterData.time?.[0]),
      end_time: this.formatDate(this.filterData.time?.[1]),
      status: this.filterData.status,
    });
  },
};
</script>
  
  <style lang="scss" scoped>
.Facial-Secondary-Review-box {
  .contentbodybox-top-r {
    width: 25%;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    .el-button {
      margin-left: 15px;
    }
  }
  .facebox {
    display: flex;
    align-items: center;
    justify-content: center;
    height: calc(100% - 100px);
    .imglist {
      width: 100%;
      height: 99%;
      display: flex;
      flex-wrap: wrap; /* 启用换行 */
      justify-content: flex-start; /* 左对齐 */
      gap: 20px; /* 增加间距 */
      padding: 15px;
      overflow: auto;
      border: 1px solid #ebeef5;
      box-sizing: border-box;

      .infoBox {
        flex: 0 0 calc((100% - 80px) / 5); /* 保证一行最多显示5个，考虑间距 */
        min-width: 180px; /* 设置最小宽度，避免太窄 */
        max-height: 247px;
        box-shadow: 0 1px 10px 0 rgba(0, 0, 0, 0.17);
        border-radius: 3px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        padding: 5px 5px 10px 5px;
        box-sizing: border-box;
        .imgBox {
          min-height: 118px;
          height: 118px;
          width: 100%;
          border: 0.7px dashed rgba(24, 144, 255, 0.78);
          border-radius: 2px;
          display: flex;
          align-items: center;
          justify-content: center;
          img {
            cursor: pointer;
            width: 100%;
            height: 100%;
            object-fit: contain;
          }
        }
        .infoTextBox {
          width: 100%;
          box-sizing: border-box;
          display: flex;
          justify-content: center;
          font-size: 12px;
          font-weight: 500;
          color: rgba(0, 0, 0, 0.65);
          .info-l,
          .info-r {
            display: flex;
            flex-direction: column;
          }
          .info-l {
            display: flex;
            align-items: center;
            justify-content: center;
            align-items: flex-end;
            margin-right: 20px;

            span {
              font-weight: bold;
            }
          }
          .info-r {
            .no_fake {
              color: #81bf49;
            }
            .is_fake {
              color: #e17470;
            }
            .reason{
              color: #609efa;
            }
          }
        }
        .buttonBox {
          margin: 10px 0;
          width: 100%;
          display: flex;
          justify-content: space-around;
        }
      }
    }
  }
}

</style>