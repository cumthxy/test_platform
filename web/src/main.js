import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'
import ElementPlus from 'element-plus';
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'element-plus/dist/index.css'

// 统一导入el-icon图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'


// 注册icon图标
const app = createApp(App)
for (let iconName in ElementPlusIconsVue) {
  app.component(iconName, ElementPlusIconsVue[iconName])
}

app.use(ElementPlus, {
  locale: zhCn,
})
app.use(router).mount('#app')

