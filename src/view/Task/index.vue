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
      :row-class-name="tableRowClassName"
      :header-cell-style="{
        background: '#f5f7f9',
      }"
      :row-style="{
        height: '65px',
      }"
      border
    >
      <el-table-column width="50" type="expand">
        <template #default="props">
          <div class="stepBox">
            <el-steps :active="1" style="width: 900px" align-center>
              <el-step title="Step 1" />
              <el-step title="Step 2" />
              <el-step title="Step 3" />
              {{ props.data }}
            </el-steps>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="id" label="任务id" align="center" />
      <el-table-column prop="task_name" label="任务名称" align="center" />
      <el-table-column prop="uname" label="客户名称" align="center" />
      <el-table-column prop="status" label="最新状态" align="center" />
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
                <el-dropdown-item>执行</el-dropdown-item>

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
                  @click="donwLoad(scope.row.id)"
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
    destroy-on-close
    width="550px"
  >
    <TaskAlert :modifyData="modifyData" @closeAlert="closealert" />
  </el-dialog>
</template>

<script>
import "@/style/content.min.css";
import TaskAlert from "./TaskAlert/index.vue";
import { getTasklist, DelTasklist, downFile } from "@/api/api";
export default {
  components: {
    TaskAlert,
  },
  data() {
    return {
      options: [
        {
          value: "1",
          label: "待调度",
        },
        {
          value: "2",
          label: "执行中",
        },
        {
          value: "3",
          label: "成功",
        },
        {
          value: "4",
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
      TaskStatus: false,
      modifyData: null,
    };
  },
  methods: {
    // 下拉窗口class类名判断
    tableRowClassName({ row }) {
      return row.status === "执行中" ? "" : "noselect"; // 为 name 为 'Tom' 的行添加 'noselect' 类
    },
    search() {},
    openAlert({ type, data }) {
      this.TaskStatus = true;
      if (type === 1) {
        this.modifyData = null;
      } else {
        // 修改
        this.modifyData = data;
        console.log(this.modifyData);
      }
    },
    closealert() {
      this.TaskStatus = false;
      this.getDatalist();
    },
    handleCurrentChange(val) {},
    handleSizeChange(val) {},

    // 下载测试结果文件
    donwLoad(id) {
      downFile({ id }).then((res)=>{
        console.log(res)
        // const link = document.createElement('a');
        // link.href = info.filename
        // link.target = '_blank'; // 如果需要在新标签页打开，可以设置 target
        // link.setAttribute('download', info.filename || 'downloaded_file'); // 设置文件名（可选）
        // document.body.appendChild(link);
        // link.click(); // 模拟点击触发下载
        // document.body.removeChild(link); // 移除 DOM 节点;
      });
    },

    // 删除任务
    removeData(row) {
      console.log(row.id);
      DelTasklist({ id: row.id }).then((res) => {
        console.log(res);
        if (res.re_code == 200) {
          this.$message.success("成功删除任务");
          this.getDatalist();
        }
      });

      this.$refs[`removeCode${row.date}`].hide();
    },
    getDatalist(obj) {
      getTasklist({ obj }).then((res) => {
        if (res.re_code == 200) {
          this.tableData = res.msg;
        }
      });
    },
  },
  mounted() {
    this.getDatalist();
  },
};
</script>

<style lang="scss">
.noselect {
  .el-table__expand-icon {
    display: none;
  }
}
.stepBox {
  display: flex;
  justify-content: center;
  align-items: center;
}
// .cell {
//   cursor: pointer;
//   display: flex;
//   align-items: center;
//   justify-content: center;
// }
</style>