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
        name: "layout-default",
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
      },     {
        path: '/layout/Office-face',
        name: 'Office-face',
        component: () => import('../view/office-face/index.vue'),
        meta: {
          title: "Office face",
          breadcrumb: ["Home", "Office face"],
          icon: "Document", // 图标名称
        },
      },
      {
        path: '/layout/FakeFaceConfirm',
        name: 'Fake_face_confirm',
        component: () => import('../view/FakeFaceConfirm/index.vue'),
        meta: {
          title: "Fake_face_confirm",
          breadcrumb: ["Home", "Fake_face_confirm"],
          icon: "User", // 图标名称
        },
      },
      
      {
        path: '/layout/FaceCard',
        name: 'FaceCard',
        component: () => import('../view/FakeCard/index.vue'),
        meta: {
          title: "Fake_card_confirm",
          breadcrumb: ["Home", "Fake_card_confirm"],
          icon: "Postcard", // 图标名称
        },
      },
      // {
      //   path: '/layout/faceOcr',
      //   name: 'faceOcr',
      //   component: () => import('../view/faceOcr/index.vue'),
      //   meta: {
      //     title: "风险人脸",
      //     breadcrumb: ["首页", "风险人脸搜索"],
      //     icon: "VideoCamera", // 图标名称
      //   },
      // },
   
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
