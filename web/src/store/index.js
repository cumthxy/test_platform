import { createStore } from 'vuex';
import imgPreview from './modules/imgPreview';

const store = createStore({
  modules: {
    imgPreview,
  },
});

export default store;
