<template>
  <div>
    <el-row style="margin-top: 20px">
      <el-col :span="24">
        <el-card :header="'mx_phone'">
          <el-row :gutter="12">
            <el-col :span="16">
              <el-input v-model="mx_phone" placeholder="mx_Phone Value" />
            </el-col>
            <el-col :span="8">
              <el-button
                @click="handleDecrypt('mx_phone', mx_phone)"
                type="primary"
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
              <el-button @click="handleDecrypt('id_phone', id_phone)" type="primary">
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
                @click="handleDecrypt('id_ktp', id_ktp)"
                type="primary"
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
    };
  },
  methods: {
   async handleDecrypt(type, str) {
  const res = await Md5decode({ md5_type: type, value: str });

  if (res.re_code === 200) {
    const resultMap = {
      phone: 'mx_phoneResult',
      ktp: 'id_phoneResult',
      id_ktp: 'id_ktpResult',
    };

    if (resultMap[type]) {
      this[resultMap[type]] = res.msg; // 动态设置结果
    }
  }
}
  },
};
</script>
  
  <style scoped>
.el-col {
  margin-bottom: 40px;
}
/* 添加一些样式 */
</style>
  