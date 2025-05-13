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
      <!-- 动态生成导航栏 -->
      <div class="menubox">
        <el-menu-item
          v-for="menu in menuRoutes"
          :key="menu.path"
          :index="menu.path"
        >
          <el-icon>
            <component :is="menu.meta.icon" />
          </el-icon>
          <template #title>{{ menu.meta.title }}</template>
        </el-menu-item>
        
      </div>
    </div>

    <div class="btn-box">
      <div class="toggle-button" @click="isCollapse = !isCollapse">
        <el-icon>
          <Right v-if="isCollapse" />
          <Back v-else />
        </el-icon>
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
          <div class="title-btn">
            <el-button @click="Notice.status = true"
            ><el-icon><Flag /></el-icon>公告</el-button
          >
          <el-button @click="logout"
            >退出登录</el-button
          >
          </div>
        </div>
        <router-view />
      </div>
    </div>

    <el-dialog v-model="Notice.status" title="公告" width="500">
      <div
        style="min-height: 300px; font-size: 14px"
        v-html="Notice.text"
      ></div>
    </el-dialog>
  </div>
</template>
  <script >
import "./layout.min.css";
import "@/style/content.min.css";
import { staticRoute } from "../../router/staic-route";
import { announcement } from "@/api/api";
export default {
  data() {
    return {
      activeMenu: this.$route.path,
      isCollapse: true,
      Notice: {
        text: null,
        status: false,
      },
      menuRoutes: [],
    };
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
  },
  mounted() {
    const layoutRoute = staticRoute.find((route) => route.path === "/layout");
    if (layoutRoute && layoutRoute.children) {
      // 过滤出有 meta.title 的路由作为菜单项
      this.menuRoutes = layoutRoute.children.filter(
        (child) => child.meta && child.meta.title
      );
    }
    this.Notice.status = true;
    announcement().then((res) => {
      this.Notice.text = res.msg.replace(/\n/g, "<br/>");
    });
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
  .title-btn {
    .el-button {
      background-color: #f5f7f9;
      color: #4370ca;
      padding: 8px 10px;
    }
  }
}
</style>