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
          @change="statusChange"
        >
          <el-option
            v-for="item in option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>

        <el-button @click="search">Search</el-button>
        <span class="tip">Delete blur, fake, no_face, fake_face</span>
      </div>
      <div class="contentbodybox-top-r">
        <el-checkbox
          label="Check All"
          size="large"
          v-model="checkAll"
          :indeterminate="isIndeterminate"
          @change="CheckAllChange"
        />
        <div class="button-box">
          <el-button
            v-if="
              filterData.status == 'pending' || filterData.status == 'delete'
            "
            @click="uploadArr"
            >Upload</el-button
          >
          <el-button v-if="filterData.status == 'upload'" @click="confirmArr"
            >Confirm</el-button
          >
          <el-button
            v-if="filterData.status != 'delete'"
            type="danger"
            @click="deleteArr"
            >Delete</el-button
          >
        </div>
      </div>
    </div>
    <div class="facebox" v-loading="loading">
      <ul class="imglist" v-if="list.length > 0">
        <li v-for="(item, index) in list" :key="item.id" class="infoBox">
          <el-checkbox v-model="item.checkStatus" size="large" />
          <div class="infoTextBox">
            <div class="info-l">
              <span>CreateTime</span>
              <span>NIK</span>
              <span>Status</span>
            </div>
            <div class="info-r">
              <span>{{ item.create_time }}</span>
              <span>{{ item.nik }}</span>
              <span :class="item.status">{{ item.status }}</span>
            </div>
          </div>
          <div class="imgBox">
            <img
              alt=""
              v-if="item.image_url == ''"
              :key="'empty-' + item.id"
              src="../../../public/头像.png"
            />
            <img
              alt=""
              v-else
              :key="item.image_url + '-' + item.id"
              :src="item.image_url"
              @click="openPreview(index)"
            />
          </div>
          <div class="buttonBox">
            <el-button
              type="primary"
              plain
              size="small"
              v-if="item.status == 'pending' || item.status == 'delete'"
              @click="Openupload(item)"
              >Upload</el-button
            >
            <el-button
              type="primary"
              plain
              size="small"
              v-if="item.status == 'upload'"
              @click="OpenConfirm(item)"
              >Confirm</el-button
            >
            <el-button
              type="danger"
              plain
              size="small"
              v-if="item.status != 'delete'"
              @click="Opendelete(item)"
              >Delete</el-button
            >
          </div>
        </li>
      </ul>

      <el-empty description="No data available at the moment" :image-size="200" v-else />
    </div>
    <div class="Pagination-box">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        v-model:current-page="currentPage"
        :page-sizes="[20, 30, 40]"
        :page-size="pagesize"
        layout="sizes, prev, pager, next"
        :total="total"
      >
      </el-pagination>
    </div>
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="400"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <span>{{ dialogContent }}</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button size="small" @click="handleCancel">No</el-button>
          <el-button
            size="small"
            type="primary"
            :loading="buttonLoad"
            @click="handleConfirm"
          >
            Yes
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import {
  getofficeFace,
  UploadOfficeFace,
  DelOfficeFace,
  confirmOfficeFace,
} from "@/api/api.js";
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
        { value: "pending", label: "pending" },
        { value: "upload", label: "upload" },
        { value: "delete", label: "delete" },
        { value: "final_state", label: "final_state" },
      ],
      dialogVisible: false,
      dialogTitle: "",
      dialogContent: "",
      dialogType: "", // 'upload', 'delete', 'confirm'
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
    statusChange() {
      this.search();
    },
    openPreview(index) {
      let urlList = this.list.map((item, index) => {
        return item.image_url; // 添加唯一标识
      });
      this.$hevueImgPreview({
        multiple: true,
        nowImgIndex: index,
        imgList: urlList,
        dataList: this.list,
        type: "",
        onupload: (data) => {
          this.Openupload(data.dataUrl);
        },
        ondelete: (data) => {
          this.Opendelete(data.dataUrl);
        },
      });
    },

    closePreview() {
      this.$store.commit("SET_VISIBLE", false);
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
    openDialog(type, data) {
      this.dialogType = type;
      this.AlertDataArr = Array.isArray(data) ? data : [data];

      switch (type) {
        case "upload":
          this.dialogTitle = "Upload Tips";
          this.dialogContent = "Are you sure to upload?";
          break;
        case "delete":
          this.dialogTitle = "Delete Tips";
          this.dialogContent = "Are you sure to delete?";
          break;
        case "confirm":
          this.dialogTitle = "Confirm Tips";
          this.dialogContent = "Are you sure to confirm?";
          break;
      }

      this.dialogVisible = true;
    },

    // 取消操作
    handleCancel() {
      this.dialogVisible = false;
      this.buttonLoad = false;
    },

    // 确认操作
    handleConfirm() {
      switch (this.dialogType) {
        case "upload":
          this.Upload();
          break;
        case "delete":
          this.DelData();
          break;
        case "confirm":
          this.confirmData();
          break;
      }
    },

    // 多选上传
    uploadArr() {
      let filterArr = this.list.filter((item) => item.checkStatus === true);
      this.Openupload(filterArr);
    },
    // 修改原有的方法调用
    Openupload(data) {
      this.openDialog("upload", data);
    },

    deleteArr() {
      let filterArr = this.list.filter((item) => item.checkStatus === true);
      this.Opendelete(filterArr);
    },
    //删除
    Opendelete(data) {
      this.openDialog("delete", data);
    },
    confirmArr() {
      let filterArr = this.list.filter((item) => item.checkStatus === true);
      this.OpenConfirm(filterArr);
    },
    OpenConfirm(data) {
      this.openDialog("confirm", data);
    },

    Upload() {
      this.buttonLoad = true;
      let arr = this.AlertDataArr.map((item) => {
        return {
          image_id: item.image_id,
          image_md5: item.image_md5,
          nik: item.nik,
        };
      });

      UploadOfficeFace({
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

            this.dialogVisible = false;
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
    DelData() {
      
      this.buttonLoad = true;
      let arr = this.AlertDataArr.map((item) => {
        return {
          image_id: item.image_id,
          image_md5: item.image_md5,
          nik: item.nik,
        };
      });
      DelOfficeFace({
        bacth_list: arr,
        delete_status: this.filterData.status,
      }).then((res) => {
        if (res.re_code == 200) {
          this.$message.success(res.msg);
          arr.forEach((item) => {
            const index = this.list.findIndex(
              (listItem) => listItem.image_id === item.image_id
            );
            if (index !== -1) {
              this.list.splice(index, 1);
            }
          });
          this.closePreview();
          this.dialogVisible = false;
          this.buttonLoad = false;
        }
      });
    },
    confirmData() {
      this.buttonLoad = true;
      let arr = this.AlertDataArr.map((item) => {
        return {
          image_id: item.image_id,
          image_md5: item.image_md5,
          nik: item.nik,
        };
      });
      confirmOfficeFace({
        bacth_list: arr,
      }).then((res) => {
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

          this.dialogVisible = false;
          this.buttonLoad = false;
        }
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
      threeDaysAgo.setDate(today.getDate() - 30); // 设置为前三天
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
      let res = await getofficeFace(obj);
      if (res.re_code == 200) {
        this.isIndeterminate = false;
        this.checkAll = false;
        this.list = res.msg.data.map((item) => {
          return {
            ...item,
            checkStatus: false,
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
  .contentbodybox-top-l {
    width: 75%;
    .tip {
      margin-left: 10px;
      display: flex;
      align-items: center;
      color: red;
      font-weight: bold;
    }
  }
  .contentbodybox-top-r {
    width: 20%;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    .button-box {
      margin-left: 20px;
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
      gap: 10px; /* 添加子元素间距，替代 margin */
      overflow: auto;
      border: 1px solid #ebeef5;
      box-sizing: border-box;

      .infoBox {
        flex: 0 0 calc((100% - 140px) / 5); /* 保证一行显示 5 个，减去 gap */
        margin: 10px 10px 10px 10px;
        max-height: 247px;
        box-shadow: 0 1px 10px 0 rgba(0, 0, 0, 0.17);
        border-radius: 3px;
        display: flex;
        align-items: center;
        flex-direction: column;
        align-items: flex-start;
        padding: 0px 5px 10px 5px;
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
            .upload {
              color: #40a9ff;
            }
            .delete {
              color: #e17470;
            }
            .final_state {
              color: #81bf49;
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
.viewerPostion {
  position: relative;
}
</style>