<template>
  <div>
    <el-row>
      <el-col :span="24">
        <el-card :header="'mx_phone'">
          <el-row :gutter="12">
            <el-col :span="16">
              <el-input v-model="mx_phone" placeholder="mx_Phone Value" />
            </el-col>
            <el-col :span="8">
              <el-button
                @click="handleDecrypt('mx_phone', mx_phone)"
                :disabled="mx_phone ? false : true"
                type="primary"
                :loading="mx_phoneLoading"
              >
                解码
              </el-button>
            </el-col>
          </el-row>
          <div style="margin-top: 10px">结果: {{ mx_phoneResult }}</div>
        </el-card>
      </el-col>

      <el-col :span="24">
        <el-card :header="'id_phone'">
          <el-row :gutter="12">
            <el-col :span="16">
              <el-input v-model="id_phone" placeholder="id_phone Value" />
            </el-col>
            <el-col :span="8">
              <el-button
                :disabled="id_phone ? false : true"
                @click="handleDecrypt('id_phone', id_phone)"
                type="primary"
                :loading="id_phoneLoading"
              >
                解码
              </el-button>
            </el-col>
          </el-row>
          <div style="margin-top: 10px">结果: {{ id_phoneResult }}</div>
        </el-card>
      </el-col>

      <el-col :span="24">
        <el-card :header="'id_ktp'">
          <el-row :gutter="12">
            <el-col :span="16">
              <el-input v-model="id_ktp" placeholder="id_ktp Value" />
            </el-col>
            <el-col :span="8">
              <el-button
                :disabled="id_ktp ? false : true"
                @click="handleDecrypt('id_ktp', id_ktp)"
                type="primary"
                :loading="id_ktpLoading"
              >
                解码
              </el-button>
            </el-col>
          </el-row>
          <div style="margin-top: 10px">结果: {{ id_ktpResult }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
  
<script>
import { Md5decode } from "@/api/api.js";
export default {
  data() {
    return {
      mx_phone: "",
      id_phone: "",
      id_ktp: "",
      mx_phoneResult: "",
      id_phoneResult: "",
      id_ktpResult: "",
      mx_phoneLoading: false,
      id_phoneLoading: false,
      id_ktpLoading: false,
    };
  },
  methods: {
    async handleDecrypt(type, str) {
      const loadingVar = `${type}Loading`;
      const resultVar = `${type}Result`;
      this[loadingVar] = true;
      this[resultVar] = "";

      try {
        const res = await Md5decode({ md5_type: type, value: str });
        if (res.re_code === 200) {
          const resultMap = {
            mx_phone: "mx_phoneResult",
            id_phone: "id_phoneResult",
            id_ktp: "id_ktpResult",
          };
          if (resultMap[type]) {
            this[resultMap[type]] = res.msg;
          }
        } else {
          const resultMap = {
            mx_phone: 'mx_phoneResult',
            id_phone: 'id_phoneResult',
            id_ktp: 'id_ktpResult',
          };
          if (resultMap[type]) {
            this[resultMap[type]] = res.msg || "解码失败";
          }
        }
      } catch (error) {
        console.error("Decode error:", error);
        const resultMap = {
          mx_phone: "mx_phoneResult",
          id_phone: "id_phoneResult",
          id_ktp: "id_ktpResult",
        };
        if (resultMap[type]) {
          this[resultMap[type]] = "解码失败";
        }
      } finally {
        this[loadingVar] = false;
      }
    },
  },
};
</script>
  
<style scoped>
.el-col {
  margin-bottom: 40px;
}
/* 添加一些样式 */
</style>
  