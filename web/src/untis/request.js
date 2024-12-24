
import axios from "axios"
import { ElMessage } from 'element-plus';
import router from '@/router' // 导入router对象
const request = axios.create({
    baseURL: `https://data.abckyc.online/v1`,
      // 网络请求多久结束
      timeout: 30000
})
// 请求拦截器
request.interceptors.request.use((config) => {
    config.headers['Authorization'] ='Bearer  '+JSON.parse(window.localStorage.getItem("token"))
    return config
})

request.interceptors.response.use(
    (response) => {
        if (response.config.responseType === 'blob') {
            return response;
        }
        if (response.data.re_code == 401) {
            ElMessage.warning(response.data.msg)
        }else if (response.data.re_code == 500){
            ElMessage.error(response.data.msg)
        }
        return response.data;
    },
    (error) => {
        if (router.currentRoute.path !== '/login'&&error.response && error.response.status === 401) {
            // 执行拦截操作，例如跳转到登录页面
            router.push("/login");
          }else if (error.code === 'ECONNABORTED' && error.message.indexOf('timeout') !== -1) {
            ElMessage.error("Request timed out!");
        }
        // 其他错误
        else {
            ElMessage.error(error.message || "An error occurred!");
        }

    }
);

export default request
