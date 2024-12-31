<template>
  <div class="content-box Facial-Secondary-Review-box">
    <div class="contentbodybox-top">
      <div class="contentbodybox-top-l">
        <el-date-picker
          v-model="filterData.time"
          type="daterange"
          range-separator="至"
          start-placeholder="开始时间"
          end-placeholder="结束时间"
        />
        <el-select
          placeholder="状态"
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

        <el-button @click="search">搜索</el-button>
      </div>
    </div>
    <div class="facebox" v-loading="loading">
      <ul class="imglist" v-if="list.length>0">
        <li v-for="item in list" :key="item.id" class="infoBox">
          <div class="infoTextBox">
            <div class="info-l">
              <span>创建时间</span>
              <span>NIK</span>
              <span>状态</span>
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
              src="../../../public/头像.png"
            />
            <img alt="" v-else :src="item.image_url" />
          </div>
          <div class="buttonBox" v-if="item.status != 'upload'">
            <el-button
              type="primary"
              plain
              size="small"
              @click="Openupload(item)"
              >上传</el-button
            >
            <el-button
              type="danger"
              plain
              size="small"
              v-if="item.status != 'delete'"
              @click="Opendelete(item)"
              >删除</el-button
            >
          </div>
        </li>
      </ul>
      
        <el-empty   :image-size="200"  v-else />

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
      v-model="UploadAlertStatus"
      title="上传提醒"
      width="400"
      :before-close="handleClose"
    >
      <span>确定上传吗</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button size="small" @click="UploadAlertStatus = false"
            >取消</el-button
          >
          <el-button
            size="small"
            type="primary"
            :loading="buttonLoad"
            @click="Upload"
          >
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
    <el-dialog v-model="DelAlertStatus" title="删除提醒" width="400">
      <span>确定删除吗</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button size="small" @click="DelAlertStatus = false"
            >取消</el-button
          >
          <el-button
            size="small"
            type="primary"
            :loading="buttonLoad"
            @click="DelData"
          >
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>

    <el-image-viewer
    v-if="visible"
    :url-list="urlList"
    :initial-index="0"
    @close="visible = false"
    class="viewerbox"
  >
    <!--定位-->
    <div class="viewerPostion">
      <button @click="downloadImage">上传</button>
      <button @click="shareImage">删除</button>
    </div>
  </el-image-viewer>
  </div>
</template>

<script>
import { getofficeFace, UploadOfficeFace, DelOfficeFace } from "@/api/api.js";
export default {
  data() {
    return {
      visible: false,
      urlList: [
        '../../../public/测试人脸.jpg',
        '../../../public/测试证件.jpg'
      ],
      filterData: {
        time: [],
        status: "",
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
      ],
      UploadAlertStatus: false,
      DelAlertStatus: false,
      buttonLoad: false,
      AlertData: {}, //用于弹窗后的确定传参
    };
  },
  methods: {
    // 删除
    Openupload(item) {
      this.AlertData = item;
      this.UploadAlertStatus = true;
    },
    Opendelete(item) {
      this.AlertData = item;
      this.DelAlertStatus = true;
    },
    Upload() {
      this.buttonLoad = true;
      UploadOfficeFace({
        image_id: this.AlertData.image_id,
        image_md5: this.AlertData.image_md5,
        nik: this.AlertData.nik,
      }).then((res) => {
        console.log(res);
        if (res.re_code == 200) {
          this.$message.success(res.msg);
          // 根据image_id在list中筛选 找到之后将这条数据在list中删除
          const index = this.list.findIndex(
            (item) => item.image_id === this.AlertData.image_id
          );
          if (index !== -1) {
            this.list.splice(index, 1);
          }
          this.UploadAlertStatus = false;
          this.buttonLoad = false;
        }
      });
    },
    DelData() {
      this.buttonLoad = true;
      DelOfficeFace({
        image_id: this.AlertData.image_id,
        image_md5: this.AlertData.image_md5,
        nik: this.AlertData.nik,
      }).then((res) => {
        console.log(res);
        if (res.re_code == 200) {
          this.$message.success(res.msg);
          const index = this.list.findIndex(
            (item) => item.image_id === this.AlertData.image_id
          );
          if (index !== -1) {
            this.list.splice(index, 1);
          }
          this.DelAlertStatus = false;
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
    getTodayRange() {
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, "0");
      const day = String(today.getDate()).padStart(2, "0");
      const todayString = `${year}-${month}-${day}`;
      return [todayString, todayString]; // 返回 [开始时间, 结束时间]
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
        this.list = res.msg.data;
        this.total = res.msg.total;
      }
      this.loading = false;
    },
  },
  mounted() {
    this.filterData.time = this.getTodayRange();
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

  .facebox {
    display: flex;
    align-items: center;
    justify-content: center;
    height: calc(100% - 100px);
    .imglist {
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
        padding: 20px 5px 10px 5px;
        box-sizing: border-box;
        .imgBox {
          height: 118px;
          width: 100%;
          border: 0.7px dashed rgba(24, 144, 255, 0.78);
          border-radius: 2px;
          display: flex;
          align-items: center;
          justify-content: center;
          img {
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
              color: #81bf49;
            }
            .delete {
              color: #e17470;
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
.viewerPostion{
  position: relative;
}
</style>