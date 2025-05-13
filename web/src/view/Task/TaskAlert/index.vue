<template>
  <div>
    <el-form
      ref="alertForm"
      style="max-width: 600px"
      :model="ruleForm"
      :rules="rules"
      label-width="auto"
      class="demo-ruleForm"
      status-icon
    >
      <el-form-item label="任务名称" prop="taskName">
        <el-input v-model="ruleForm.taskName" placeholder="输入任务名称" />
      </el-form-item>
      <el-form-item label="客户名称" prop="customerName">
        <el-input v-model="ruleForm.customerName" placeholder="输入客户名称" />
      </el-form-item>
      <el-form-item label="测试接口" prop="filterTemp" class="tableItem">
        <el-table
          :data="filterTempValue(this.TemplateData, this.ruleForm.filterTemp)"
          style="width: 100%; height: 70%"
          :row-style="{
            height: '30px',
          }"
          border
        >
          <el-table-column label="接口名称" align="center" prop="name" />
        </el-table>
        <div>
          <el-button size="small" type="primary" @click="AlertStatus = true"
            >接口选择</el-button
          >
        </div>
      </el-form-item>
      <el-form-item
        v-if="
          Countryjudge(
            filterTempValue(this.TemplateData, this.ruleForm.filterTemp)
          )
        "
        label="WhatsApp国家码"
        prop="country"
      >
        <el-input v-model="ruleForm.country" placeholder="输入国家码" />
      </el-form-item>
      <el-form-item label="Md5" prop="md5">
        <el-radio v-model="ruleForm.md5" label="1">是</el-radio>
        <el-radio v-model="ruleForm.md5" label="0">否</el-radio>
      </el-form-item>
      <el-form-item label="上传本地文件" prop="file">
        <el-upload
          ref="uploadRef"
          style="width: 100%"
          action=""
          :auto-upload="false"
          :on-change="fileChange"
          :on-remove="fileRemove"
          :limit="1"
          :on-exceed="handleExceed"
          :file-list="ruleForm.file"
        >
          <el-button type="primary" size="small"
            >点击上传<el-icon class="el-icon--right"><Upload /></el-icon
          ></el-button>
          <template #tip> </template>
        </el-upload>
      </el-form-item>

      <div class="footer">
        <el-button
          :disabled="isThrottled"
          type="info" 
          size="small"
          @click="$emit('closeAlert',1)"
          >关闭</el-button
        >
        <el-button
          type="primary"
          size="small"
          :loading="isThrottled"
          @click="AlertOk"
          >{{isThrottled?'提交中...':'提交'}}</el-button
        >
      </div>
    </el-form>
    <el-dialog v-model="AlertStatus" width="730" title="选择接口">
      <Transfer
        :transfer-data="TemplateData"
        :transfer-value="ruleForm.filterTemp"
        @update:left="handleAdd"
        @update:right="handleRemove"
        @clear="handleClear"
      />
      <div class="footer">
        <el-button type="primary" size="small" @click="CloseAlertson()"
          >确定</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { gettestApi, createTask, modifyTask } from "@/api/api.js";
import Transfer from "../../../components/Transfer/index.vue";
import { genFileId } from "element-plus";
export default {
  props: ["modifyData"],
  components: {
    Transfer,
  },
  data() {
    return {
      ruleForm: {
        id: null, //修改用
        taskName: "",
        customerName: "",
        file: [],
        country: "",
        md5: "1",
        filterTemp: [], //选择后的接口模版
      },
      rules: {
        taskName: [
          { required: true, message: "请输入任务名称", trigger: "blur" },
        ],
        customerName: [
          { required: true, message: "请输入客户名称", trigger: "blur" },
        ],
        filterTemp: [
          { required: true, message: "请选择接口", trigger: "change" },
        ],
        country: [{ required: true, message: "请输入国家码", trigger: "blur" }],
        md5: [{ required: true, message: "请选择md5", trigger: "blur" }],
        file: [{ required: true, message: "请上传文件", trigger: "blur" }],
      },
      TemplateData: [], //模板列表（接口）
      AlertStatus: false,
      isThrottled: false, //节流阀
    };
  },
  methods: {
    handleExceed(files) {
      const upload = this.$refs.uploadRef;
      // 清除文件
      upload.clearFiles();
      // 获取第一个文件并生成 ID
      const file = files[0];
      file.uid = genFileId();
      upload.handleStart(file);
    },
    fileChange(uploadFile, fileList) {
      this.ruleForm.file[0] = uploadFile;
      if (fileList.length !== 0) {
        this.$refs.alertForm.validateField("file");
      }
    },
    fileRemove(uploadFile, fileList) {
      if (fileList.length === 0) {
        this.ruleForm.file = [];
        this.$refs.alertForm.validateField("file");
      }
    },

    // 穿梭框相关
    handleAdd(key) {
      if (!this.ruleForm.filterTemp.includes(key)) {
        this.ruleForm.filterTemp.push(key);
      }
    },
    handleRemove(key) {
      const index = this.ruleForm.filterTemp.indexOf(key);
      if (index !== -1) {
        this.ruleForm.filterTemp.splice(index, 1);
      }
    },
    handleClear() {
      this.ruleForm.filterTemp = [];
    },

    Countryjudge(arr) {
      if (arr.some((item) => item.name.includes("全球WhatsApp"))) {
        return true;
      } else {
        this.ruleForm.country = "";
        return false;
      }
    },
    // 根据选择的接口id 选择
    filterTempValue(templateData, selectTemplateArr) {
      // 将 selectTemplateArr 转换为普通数组，便于操作
      const selectedValues = Array.from(selectTemplateArr);
      // 使用 filter 筛选出符合条件的数据
      const filteredData = templateData.filter((item) =>
        selectedValues.includes(item.id)
      );
      return filteredData;
    },
    // 关闭接口选择后的校验
    CloseAlertson() {
      if (this.ruleForm.filterTemp.length >= 1) {
        this.$refs.alertForm.validateField("filterTemp");
      } else {
        this.$refs.alertForm.validateField("filterTemp");
      }

      this.AlertStatus = false;
    },
    // 提交任务
    AlertOk() {
      this.$refs.alertForm.validate(async (valid) => {
        if (valid) {
          if (this.isThrottled) {
            return;
          }
          // 设置节流状态为true
          this.isThrottled = true;

          let filterTmplist = this.filterTempValue(
            this.TemplateData,
            this.ruleForm.filterTemp
          ).map((item) => {
            return { id: item.id, url: item.url, name: item.name };
          });
          const formData = new FormData();
          formData.append("uname", this.ruleForm.customerName); // 客户名称
          formData.append("task_name", this.ruleForm.taskName); // 任务名称
          formData.append("test_api_list", JSON.stringify(filterTmplist)); // JSON 格式的接口列表
          formData.append("is_md5", this.ruleForm.md5); // 任务名称
          if (this.ruleForm.country) {
            formData.append("country", this.ruleForm.country);
          } // 国家码

          // 修改
          if (this.modifyData) {
            formData.append("id", this.ruleForm.id); // 修改的id
            if (this.ruleForm.file[0].raw) {
              formData.append("file", this.ruleForm.file[0].raw); // 上传的文件
              formData.append("file_name", this.ruleForm.file[0].name);
            } else {
              formData.append("file_name", this.modifyData.file_name);
            }
            try {
              const response = await modifyTask(formData);
              if (response && response.re_code == 200) {
                this.$message.success("成功修改任务");
                this.$emit("closeAlert",2);
                this.isThrottled = false;
              } else {
                this.isThrottled = false;
              }
            } catch (error) {
              this.isThrottled = false;
            }
          } else {
            // 创建任务
            formData.append("file", this.ruleForm.file[0].raw); // 上传的文件
            formData.append("file_name", this.ruleForm.file[0].name);
            try {
              const response = await createTask(formData);
              if (response && response.re_code == 200) {
                this.$message.success("成功创建任务");
                this.isThrottled = false;
                this.$emit("closeAlert",2);
              } else {
                this.isThrottled = false;
              }
            } catch (error) {
              this.isThrottled = false;
            }
          }
        }
      });
    },
  },
  async mounted() {
    await gettestApi().then((res) => {
      if (res.re_code == 200) {
        this.TemplateData = res.msg;
      }
    });
    // 如果这个窗口为修改窗口
    if (this.modifyData) {
      this.ruleForm = {
        id: this.modifyData.id,
        taskName: this.modifyData.task_name,
        customerName: this.modifyData.uname,
        file: [{ name: this.modifyData.file_name, url: "" }],
        country: this.modifyData.country,
        md5: String(this.modifyData.is_md5),
        filterTemp: JSON.parse(this.modifyData.test_api_list).map(
          (item) => item.id
        ), //选择后的接口模版
      };
    }
  },
};
</script>

<style lang="scss" >
.tableItem {
  height: 250px;
  .el-table__cell {
    padding: 0px !important;
  }
}
</style>