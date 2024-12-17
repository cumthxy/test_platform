<template>
  <div class="content-box">
    <!-- form表单筛选 -->
    <div class="contentbodybox-top">
      <div class="contentbodybox-top-l">
        <el-input placeholder="接口ID/接口名称" v-model="searchValue" />
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
      :height="'calc(100% - 42px  - 20px)'"
      :header-cell-style="{
        background: '#f5f7f9',
      }"
      :row-style="{
        height: '65px',
      }"
      border
    >
      <el-table-column prop="name" label="接口名称" align="center" />
      <el-table-column prop="id" label="接口id" align="center" />
      <el-table-column prop="url" width="320" label="Url" align="center" />
      <el-table-column label="更新于" prop="create_time" align="center" />
      <el-table-column label="rtype" prop="rtype" align="center" />
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
                  @click="openAlert({ type: 2, obj: scope.row })"
                  >修改</el-dropdown-item
                >

                <el-dropdown-item>
                  <el-popover
                    placement="top"
                    trigger="click"
                    width="160"
                    :ref="`removeCode${scope.row.date}`"
                  >
                    <p>确定要删除这个接口吗</p>
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
                      1
                    </template>
                  </el-popover></el-dropdown-item
                >
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <!-- 新增任务 -->
  <el-dialog
    :close-on-click-modal="false"
    :close-on-press-escape="true"
    :title="modifyStatus ? '修改接口' : '新建接口'"
    v-model="TaskStatus"
    destroy-on-close
    width="550px"
  >
    <el-form
      ref="alertForm"
      style="max-width: 600px"
      :model="ruleForm"
      :rules="rules"
      label-width="auto"
      class="demo-ruleForm"
      status-icon
    >
      <el-form-item label="接口名称" prop="name">
        <el-input v-model="ruleForm.name" />
      </el-form-item>
      <el-form-item label="接口Url" prop="url">
        <el-input v-model="ruleForm.url" />
      </el-form-item>
      <el-form-item label="rtype" prop="rtype">
        <el-radio v-model="ruleForm.rtype" label="0">0</el-radio>
        <el-radio v-model="ruleForm.rtype" label="1">1</el-radio>
      </el-form-item>
    </el-form>
    <div class="footer">
      <el-button type="primary" size="small" @click="AlertOk">提交</el-button>
    </div>
  </el-dialog>
</template>
<script>
import "@/style/content.min.css";
import { gettestApi, settestApi,modifytestApi } from "@/api/api.js";
export default {
  data() {
    return {
      searchValue:"",
      tableData: [],
      loading: false,
      TaskStatus: false,
      modifyStatus: false,
      ruleForm: {
        name: "",
        url: "",
        rtype: "0",
        id: "",
      },
      rules: {
        name: [{ required: true, message: "请输入接口名称", trigger: "blur" }],
        url: [{ required: true, message: "请输入url", trigger: "blur" }],
        rtype: [{ required: true, message: "请选择rtype", trigger: "blur" }],
      },
    };
  },
  methods: {
    search() {
      console.log(this.searchValue);
      this.getData(this.searchValue)
      
    },
    removeData(row) {
      this.$refs[`removeCode${row.date}`].hide();
    },
    AlertOk() {
      this.$refs.alertForm.validate((valid) => {
        if (valid) {
          if (this.modifyStatus) {
            modifytestApi({
              id:this.ruleForm.id,
              name: this.ruleForm.name,
              url: this.ruleForm.url,
              rtype: Number(this.ruleForm.rtype),
            }).then((res) => {
              if (res.re_code == 200) {
                this.$message.success("成功修改接口");
                this.getData();
                this.TaskStatus = false;
              }
            });
            //修改
          } else {
            //新建
            settestApi({
              name: this.ruleForm.name,
              url: this.ruleForm.url,
              rtype: Number(this.ruleForm.rtype),
            }).then((res) => {
              if (res.re_code == 200) {
                this.$message.success("成功创建接口");
                this.getData();
                this.TaskStatus = false;
              }
            });
          }
        }
      });
    },
    openAlert(Data) {
      let { type, obj } = Data;
      this.TaskStatus = true;
      if (type == 2) {
        this.modifyStatus = true;
        this.ruleForm.name = obj.name;
        this.ruleForm.url = obj.url;
        this.ruleForm.rtype = obj.rtype;
        this.ruleForm.id = obj.id;

      } else {
        this.ruleForm = {
          name: "",
          url: "",
          rtype: "0",
          id: "",
        };
        this.modifyStatus = false;
      }
    },
    async getData(data) {
      this.loading = true;
      try {
        let res = await gettestApi(data);
        if (res) {
          this.tableData = res.msg;
          this.loading = false;
        }else{
        this.loading = false;
        }

      } catch (error) {
        this.loading = false;
      }
    },
  },
  mounted() {
    console.log(1);
    
    this.getData();
  },
};
</script>

<style lang="scss">
.active {
  .el-table__expand-icon {
    display: none;
  }
}
// .cell {
//   cursor: pointer;
//   display: flex;
//   align-items: center;
//   justify-content: center;
// }
</style>