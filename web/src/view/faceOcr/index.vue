<template>
  <div class="content-box Facial-Secondary-Review-box">
    <!-- 搜索组件 -->
    <searchInput  @search="sonSearch"/>
    <div class="facebox" v-loading="loading">
      <ul class="imglist" v-if="list.length > 0">
        <li v-for="item in list" :key="item.id" class="infoBox">
          <div class="infoTextBox">
            <div class="info-l">
              <span>相似度</span>
              <span>图片出处</span>
              <span>Nik号码</span>
              <span>Nik多投次数</span>
            </div>
            <div class="info-r">
              <span>{{ item.create_time }}</span>
              <span>{{ item.nik }}</span>
              <span :class="item.status">{{ item.status }}</span>
            </div>
          </div>
          <div class="imgBox">
            <img
              alt=""
              v-if="item.image_url == ''"
              src="../../../public/头像.png"
            />
            <img alt="" v-else :src="item.image_url" />
          </div>
        </li>
      </ul>

      <el-empty :image-size="200" v-else />
    </div>

  </div>
</template>
  
  <script>
import {} from "@/api/api.js";
import searchInput from "./searchInput/index.vue";
export default {
  components: {
    searchInput,
  },
  data() {
    return {
      currentIndex: 0,
      filterData: {
        nik: "",
        base64: "",
      },
      list: [],

      total: 0,
      loading: false,
    };
  },

  methods: {

    search() {
      this.currentPage = 1;
      this.getDataList({
        page: this.currentPage,
        page_size: this.pagesize,
      });
    },
    sonSearch(data){
      console.log(data);
      
    },
    async getDataList(obj) {
      this.loading = true;

      this.loading = false;
    },
  },
  mounted() {
    this.getDataList({});
  },
};
</script>
  
  <style lang="scss" scoped>
.Facial-Secondary-Review-box {

  .facebox {
    display: flex;
    align-items: center;
    justify-content: center;
    height: calc(100% - 100px);
    .imglist {
      width: 100%;
      height: 99%;
      display: flex;
      flex-wrap: wrap; /* 启用换行 */
      justify-content: flex-start; /* 左对齐 */
      gap: 10px; /* 添加子元素间距，替代 margin */
      overflow: auto;
      border: 1px solid #ebeef5;
      box-sizing: border-box;

      .infoBox {
        flex: 0 0 calc((100% - 140px) / 5); /* 保证一行显示 5 个，减去 gap */
        margin: 10px 10px 10px 10px;
        max-height: 247px;
        box-shadow: 0 1px 10px 0 rgba(0, 0, 0, 0.17);
        border-radius: 3px;
        display: flex;
        align-items: center;
        flex-direction: column;
        align-items: flex-start;
        padding: 0px 5px 10px 5px;
        box-sizing: border-box;
        .imgBox {
          min-height: 118px;
          width: 100%;
          border: 0.7px dashed rgba(24, 144, 255, 0.78);
          border-radius: 2px;
          display: flex;
          align-items: center;
          justify-content: center;
          img {
            cursor: pointer;
            width: 100%;
            height: 100%;
            object-fit: contain;
          }
        }
        .infoTextBox {
          width: 100%;
          box-sizing: border-box;
          display: flex;
          justify-content: center;
          font-size: 12px;
          font-weight: 500;
          color: rgba(0, 0, 0, 0.65);
          .info-l,
          .info-r {
            display: flex;
            flex-direction: column;
          }
          .info-l {
            display: flex;
            align-items: center;
            justify-content: center;
            align-items: flex-end;
            margin-right: 20px;

            span {
              font-weight: bold;
            }
          }
          .info-r {
            .upload {
              color: #81bf49;
            }
            .delete {
              color: #e17470;
            }
          }
        }
        .buttonBox {
          margin: 10px 0;
          width: 100%;
          display: flex;
          justify-content: space-around;
        }
      }
    }
  }
}

</style>