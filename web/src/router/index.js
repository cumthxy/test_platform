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
  
  next()
});
export default router