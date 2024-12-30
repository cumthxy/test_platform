<template>
  <div class="content-box">
    <!-- form表单筛选 -->
    <div class="contentbodybox-top">
      <div class="contentbodybox-top-l">
        <el-input placeholder="任务id" v-model="filterData.id" />
        <el-select
          placeholder="状态"
          v-model="filterData.status"
          style="width: 240px"
        >
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <el-input placeholder="任务名称" v-model="filterData.taskname" />
        <el-input placeholder="客户名称" v-model="filterData.customername" />
        <el-button @click="search">搜索</el-button>
      </div>
      <div class="contentbodybox-top-r">
        <el-button @click="openAlert({ type: 1 })">新建</el-button>
      </div>
    </div>
    <el-table
      class="bigtable"
      v-loading="loading"
      :data="tableData"
      style="width: 100%"
      :height="'calc(100% - 42px  - 60px)'"
      :header-cell-style="{
        background: '#f5f7f9',
      }"
      :row-style="{
        height: '65px',
      }"
      border
    >
      <el-table-column prop="id" label="任务id" align="center" />
      <el-table-column prop="task_name" label="任务名称" align="center" />
      <el-table-column prop="uname" label="客户名称" align="center" />

      <el-table-column label="最新状态" align="center">
        <template #default="scope">
          <span :class="getStatusClass(scope.row.status)">{{
            scope.row.status
          }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="create_time" label="更新于" align="center" />
      <el-table-column prop="file_name" label="文件名称" align="center" />
      <el-table-column prop="result" label="测试结果" align="center" />
      <el-table-column label="操作" align="center">
        <template #default="scope">
          <el-dropdown
            trigger="click"
            placement="bottom-end"
            class="lang-select"
            :hide-on-click="false"
          >
            <el-icon><More /></el-icon>
            <template #dropdown>
              <el-dropdown-menu class="lang-select-dropdown table-drapdown">
                <el-dropdown-item
                  @click="openAlert({ type: 2, data: scope.row })"
                  >修改</el-dropdown-item
                >
                <el-dropdown-item>
                  <el-popover
                    placement="top"
                    trigger="click"
                    width="160"
                    :ref="`removeCode${scope.row.date}`"
                  >
                    <p>确定要删除接口吗</p>
                    <div style="text-align: right; margin: 0">
                      <el-button
                        size="small"
                        text
                        @click="$refs[`removeCode${scope.row.date}`].hide()"
                        >取消</el-button
                      >
                      <el-button
                        type="primary"
                        size="small"
                        @click="removeData(scope.row)"
                        >确定</el-button
                      >
                    </div>
                    <template #reference>
                      <div size="small" style="color: red">删除</div>
                    </template>
                  </el-popover></el-dropdown-item
                >
                <el-dropdown-item
                  v-if="scope.row.result"
                  @click="donwLoad(scope.row)"
                  >下载</el-dropdown-item
                >
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>
    <div class="Pagination-box">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        v-model:current-page="currentPage"
        :page-sizes="[10, 20, 50]"
        :page-size="pagesize"
        layout="sizes, prev, pager, next"
        :total="total"
      >
      </el-pagination>
    </div>
  </div>
  <!-- 新增任务 -->
  <el-dialog
    :close-on-click-modal="false"
    :close-on-press-escape="true"
    :title="!modifyData ? '新建任务' : '修改任务'"
    v-model="TaskStatus"
    :show-close="false"
    destroy-on-close
    width="550px"
  >
    <TaskAlert
      :modifyData="modifyData"
      @closeAlert="closealert"
      :v-loading="alertLoading"
    />
  </el-dialog>
</template>

<script>
import "@/style/content.min.css";
import TaskAlert from "./TaskAlert/index.vue";
import { getTasklist, DelTasklist } from "@/api/api";
export default {
  components: {
    TaskAlert,
  },
  data() {
    return {
      options: [
        {
          value: "",
          label: "空",
        },
        {
          value: "待调度",
          label: "待调度",
        },
        {
          value: "执行中",
          label: "执行中",
        },
        {
          value: "成功",
          label: "成功",
        },
        {
          value: "失败",
          label: "失败",
        },
      ],
      filterData: {
        id: "",
        taskname: "",
        customername: "",
        status: "",
      },
      tableData: [],
      //分页，
      currentPage: 1,
      pagesize: 10,
      total: 0,
      adminUser: false,
      loading: false,
      alertLoading: true,
      TaskStatus: false,
      modifyData: null,
    };
  },
  methods: {
    // 搜索
    search() {
      this.getDatalist({
        id: this.filterData.id,
        status: this.filterData.status,
        task_name: this.filterData.taskname,
        uname: this.filterData.customername,
        page: this.currentPage,
        page_size: this.pagesize,
      });
    },
    openAlert({ type, data }) {
      this.TaskStatus = true;
      if (type === 1) {
        this.modifyData = null;
      } else {
        // 修改
        this.modifyData = data;
      }
    },
    closealert(type) {
      this.TaskStatus = false;
      console.log(type);
      if (type === 2) {
        this.getDatalist({
          id: this.filterData.id,
          status: this.filterData.status,
          task_name: this.filterData.taskname,
          uname: this.filterData.customername,
          page: this.currentPage,
          page_size: this.pagesize,
        });
      }
    },

    handleCurrentChange(val) {
      this.currentPage = val;
    },
    // 页数
    handleSizeChange(val) {
      this.pagesize = val;
    },
    getStatusClass(status) {
      switch (status) {
        case "待调度":
          return "status-pending";
        case "调度中":
          return "status-running";
        case "成功":
          return "status-success";
        case "失败":
          return "status-failed";
        default:
          return "";
      }
    },
    // 下载测试结果文件
    donwLoad(row) {
      const token = JSON.parse(window.localStorage.getItem("token")); // 获取 Token
      const fileUrl = `https://data.abckyc.online/v1/test-task/download?id=${row.id}&token=${token}`;
      // 创建一个 <a> 标签
      const link = document.createElement("a");
      link.href = fileUrl; // 设置文件地址
      link.target = "_blank"; // 如果需要新窗口打开，可以添加这一行
      link.download = row.result || "downloaded_file.xlsx"; // 设置文件名（可选）
      // 添加到 DOM 并触发点击事件
      document.body.appendChild(link);
      link.click();

      // 移除标签;
      document.body.removeChild(link);
    },

    // 删除任务
    removeData(row) {
      DelTasklist({ id: row.id }).then((res) => {
        if (res.re_code == 200) {
          this.$message.success("成功删除任务");
          this.getDatalist({
            id: this.filterData.id,
            status: this.filterData.status,
            task_name: this.filterData.taskname,
            uname: this.filterData.customername,
            page: this.currentPage,
            page_size: this.pagesize,
          });
        }
      });

      this.$refs[`removeCode${row.date}`].hide();
    },
    getDatalist(obj) {
      this.loading = true;
      getTasklist(obj).then((res) => {
        if (res.re_code == 200) {
          this.tableData = res.msg.data;
          this.total = res.msg.total;
          this.loading = false;
        }
      });
    },
  },
  mounted() {
    this.getDatalist({ page: this.currentPage, page_size: this.pagesize });
  },
};
</script>

<style lang="scss">
.stepBox {
  display: flex;
  justify-content: center;
  align-items: center;
}

.status-pending,
.status-running,
.status-success,
.status-failed {
  padding: 0px 10px;
  border-radius: 3px;
}
.status-pending {
  border: 1px solid #a7bee6;
  background-color: #e8f0fe;
}
.status-running {
  border: 1px solid #d66f35;
  background-color: #fcf6d7;
}
.status-failed {
  border: 1px solid #f9dddc;
  background-color: #fdeeee;
  color: #ec5d56;
}
.status-success {
  border: 1px solid #5fcb71;
  color: #5fcb71;
  background-color: #eaf9f1;
}
</style>