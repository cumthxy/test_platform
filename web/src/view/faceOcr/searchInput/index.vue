<template>
    <div class="search-container">
      <!-- 搜索框 -->
      <div class="search-box">
        <el-input
          v-model="inputValue"
          placeholder="请输入 NIK 或点击右侧上传"
          clearable
        >
          <!-- 右侧图标，点击后触发文件上传 -->
          <template #suffix>
            <label for="file-upload" style="display: flex; cursor: pointer;">
              <el-icon><Camera /></el-icon>
            </label>
            <input
              id="file-upload"
              type="file"
              style="display: none"
              @change="handleFileUpload"
            />
          </template>
  
          <!-- 搜索按钮 -->
          <template #append>
            <el-button @click="search">搜索</el-button>
          </template>
        </el-input>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        inputValue: "", // 输入框内容
        uploadedFile: null, // 上传的文件对象
      };
    },
    methods: {
      // 搜索逻辑
      search() {
        this.$emit('search',this.inputValue)
      },
      // 处理文件上传
      handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
          this.uploadedFile = file;
          console.log("选择的文件：", file);
          // 在这里可以上传到后端
          this.uploadFileToServer(file);
        }
      },
      // 模拟上传到后端
      uploadFileToServer(file) {
        // 假设这里是调用后端接口
        console.log("正在上传文件到后端:", file);
        // 你可以用 axios 或 fetch 上传文件
        this.$emit('search',this.uploadedFile)

      },
    },
  };
  </script>
  
  <style lang="scss">
  .search-container {
    position: relative;
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
    transition: all 0.3s ease;
    .search-box {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  }
  
 
  </style>
  