export default {
  state: () => ({
    visible: false, // 控制组件显示状态
  }),
  mutations: {
    SET_VISIBLE(state, visible) {
      state.visible = visible; // 设置 visible 状态
    },
  },
};
