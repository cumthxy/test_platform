import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig(({ mode }) => {
  // 使用 loadEnv 加载 .env 文件
  const env = loadEnv(mode, process.cwd());

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
      }
    },
    define: {
      // 通过 define 来将环境变量定义为全局常量
      'process.env': env,
    }
  };
});