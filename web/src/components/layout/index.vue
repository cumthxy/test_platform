<template>
  <div class="layout">
    <div class="menu">
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical-demo"
        :collapse="isCollapse"
        background-color="#071729"
        text-color="#fff"
        active-text-color="#ffd04b"
        unique-opened
        :router="true"
      >
        <div class="menu-top">
          <!-- 在这里写导航栏 -->
          <div class="menubox">
            <el-menu-item index="/layout/Task">
              <el-icon><Menu /></el-icon>
              <span>任务列表</span>
            </el-menu-item>
            <el-menu-item index="/layout/Template">
              <el-icon><Notebook /></el-icon>
              <span>接口列表</span>
            </el-menu-item>
            <el-menu-item index="/layout/Md5">
              <el-icon><HelpFilled /></el-icon>
              <span>Md5</span>
            </el-menu-item>
            <el-menu-item index="/layout/FaceDetection">
              <el-icon><Camera /></el-icon>
              <span>接口测试</span>
            </el-menu-item>
          </div>
        </div>

        <div class="btn-box">
          <div class="toggle-button" @click="isCollapse = !isCollapse">
            <el-icon>
              <Right v-if="isCollapse" />
              <Back v-else
            /></el-icon>
          </div>
        </div>
      </el-menu>
    </div>
    <div class="bigbox">
      <div>
        <div class="titlebox">
          <el-breadcrumb>
            <el-breadcrumb-item
              v-for="item in $route.meta.breadcrumb"
              :key="item"
            >
              {{ item }}
            </el-breadcrumb-item>
          </el-breadcrumb>
          <el-button @click="Notice.status = true"
            ><el-icon><Flag /></el-icon>公告</el-button
          >
        </div>
        <router-view />
      </div>
    </div>

    <el-dialog v-model="Notice.status" title="公告" width="500">
      <div style="min-height: 300px;font-size: 14px;"  v-html="Notice.text">

      </div>
    </el-dialog>
  </div>
</template>
  <script >
import "./layout.min.css";
import { announcement} from '@/api/api'
export default {
  data() {
    return {
      activeMenu: this.$route.path,
      isCollapse: true,
      Notice:{
        text:null,
        status:false,
      },
      
    };
  },
  mounted() {
    this.Notice.status=true
     announcement().then((res)=>{      
  this.Notice.text=res.msg.replace(/\n/g, '<br/>')     
     })
  },
};
</script>
  
  
  <style lang="scss">
.titlebox {
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  box-sizing: border-box;
  margin-bottom: 10px;
}

.titlebox {
  .title {
    font-weight: bolder;
  }

  > div:nth-child(2) {
    .el-button {
      background-color: #f5f7f9;
      color: #4370ca;
      padding: 8px 10px;
    }
  }
}
</style>