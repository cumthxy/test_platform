export const staticRoute = [
  {
    path: "/",
    redirect: "/layout",
  },
  {
    path: '/layout',
    name: "layout",
    component: () => import('../components/layout/index.vue'),
    children: [
      {
        path: "",
        redirect: '/layout/Task',
      },
      {
        path: '/layout/Task',
        name: 'Task',
        component: () => import('../view/Task/index.vue'),
        meta: {
          title: "任务列表",
          breadcrumb: ["首页", "任务列表"],
          icon: "Menu", // 图标名称
        },
      },
      {
        path: '/layout/Template',
        name: 'Template',
        component: () => import('../view/Template/index.vue'),
        meta: {
          title: "接口列表",
          breadcrumb: ["首页", "接口列表"],
          icon: "Notebook", // 图标名称
        },
      },
      {
        path: '/layout/Md5',
        name: 'md5',
        component: () => import('../view/md5/index.vue'),
        meta: {
          title: "MD5",
          breadcrumb: ["首页", "MD5"],
          icon: "HelpFilled", // 图标名称
        },
      },
      {
        path: '/layout/FaceDetection',
        name: 'FaceDetection',
        component: () => import('../view/FaceDetection/index.vue'),
        meta: {
          title: "接口测试",
          breadcrumb: ["首页", "接口测试"],
          icon: "Camera", // 图标名称
        },
      },
    ],
  },
  {
    path: '/login',
    name: "login",
    component: () => import('../view/login/index.vue'),
    meta: {
      title: "登录",
     
    },
  },
];
