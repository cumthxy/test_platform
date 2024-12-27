import { createRouter, createWebHashHistory } from 'vue-router'
import { staticRoute } from './staic-route' //静态路由
const router = createRouter({
  history: createWebHashHistory(),
  routes: staticRoute
})

router.beforeEach(async (to, from, next) => {
  let token = localStorage.getItem('token');
  if(!token && to.path != "/login"){
    next('/login');
    return;
  }
  if (to.meta.title) { //判断是否有标题
    document.title = to.meta.title //给相应页面添加标题
  }
  next()
});
export default router