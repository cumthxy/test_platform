<template>
  <transition name="fade">
    <div
      class="hevue-imgpreview-wrap"
      id="hevue-imgpreview-wrap"
      v-if="$store.state.imgPreview.visible"
      ref="heImg"
      @mouseup="removeMove('pc')"
      @touchend="removeMove('mobile')"
      @click.stop="clickMask"
    >
      <div class="he-img-wrap">
        <div
          class="heimgfont hevue-img-status-icon rotate-animation"
          v-show="imgState === 1"
        >
          &#xe6b1;
        </div>
        <!-- <div class="heimgfont loading">&#xe6b1;</div> -->
        <img
          :src="imgurl"
          ref="heImView"
          @click.stop=""
          v-show="imgState === 2"
          class="he-img-view"
          :style="
            'transform: scale(' +
            imgScale +
            ') rotate(' +
            imgRotate +
            'deg);margin-top:' +
            imgTop +
            'px;margin-left:' +
            imgLeft +
            'px;' +
            maxWH
          "
          @mousedown="addMove"
          @touchstart="addMoveMobile"
        />
        <!-- 图片加载失败 -->
        <div class="heimgfont hevue-img-status-icon" v-show="imgState === 3">
          &#xec0d;
        </div>
        <!-- 关闭按钮 -->
        <div
          class="heimgfont he-close-icon"
          @click.stop="close({ way: 'closeBtn' })"
          v-if="closeBtn"
        >
          &#xe608;
        </div>
        <!-- 左箭头 -->
        <div
          class="arrow arrow-left heimgfont"
          @click.stop="toogleImg(false, 'btn')"
          v-if="arrowBtn && multiple && imgIndex + 1 != 1"
        >
          &#xe620;
        </div>
        <!-- 右箭头 -->
        <div
          class="arrow arrow-right heimgfont"
          @click.stop="toogleImg(true, 'btn')"
          v-if="arrowBtn && multiple && imgIndex + 1 != imgList.length"
        >
          &#xe60d;
        </div>
        <!-- 控制条 -->
        <div class="he-control-bar-wrap" v-if="controlBar">
          <div class="he-control-bar" @click.stop>
            <div
              class="he-control-btn heimgfont"
              @click.stop="toogleImg(false, 'btn')"
              v-if="arrowBtn && multiple && imgIndex + 1 != 1"
            >
              &#xe620;
            </div>
            <!-- 右箭头 -->
            <div
              class="he-control-btn heimgfont"
              @click.stop="toogleImg(true, 'btn')"
              v-if="arrowBtn && multiple && imgIndex + 1 != imgList.length"
            >
              &#xe60d;
            </div>

            <!-- 缩小 -->
            <div
              class="he-control-btn heimgfont"
              @click.stop="scaleFunc(-0.15)"
            >
              &#xe65e;
            </div>
            <!-- 放大 -->
            <div class="he-control-btn heimgfont" @click.stop="scaleFunc(0.15)">
              &#xe65d;
            </div>
            <!-- 复位 -->
            <div
              class="he-control-btn heimgfont"
              v-show="isFull"
              @click.stop="imgToggle"
            >
              &#xe698;
            </div>
            <!-- 复位 -->
            <div
              class="he-control-btn heimgfont"
              v-show="!isFull"
              @click.stop="imgToggle"
            >
              &#xe86b;
            </div>
            <!-- <div class="he-control-btn heimgfont" @click.stop="rotateFunc(-90)">
              &#xe670;
            </div>
            <div class="he-control-btn heimgfont" @click.stop="rotateFunc(90)">
              &#xe66f;
            </div>
            <div class="he-control-btn heimgfont" @click.stop="downloadIamge">
              &#xe694;
            </div> -->
            <!-- 添加自定义按钮 -->
            <template v-if="type != 'fake'">
              <template v-if="dataList[nowImgIndex]?.status != 'upload'">
                <div class="he-control-btn heimgfont">
                  <svg
                    @click="customUpload"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 1024 1024"
                  >
                    <path
                      fill="currentColor"
                      d="M160 832h704a32 32 0 1 1 0 64H160a32 32 0 1 1 0-64m384-578.304V704h-64V247.296L237.248 490.048 192 444.8 508.8 128l316.8 316.8-45.312 45.248z"
                    ></path>
                  </svg>
                </div>
                <div
                  class="he-control-btn heimgfont"
                  v-if="dataList[nowImgIndex]?.status != 'delete'"
                >
                  <svg
                    @click="customDelete"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 1024 1024"
                  >
                    <path
                      fill="currentColor"
                      d="M160 256H96a32 32 0 0 1 0-64h256V95.936a32 32 0 0 1 32-32h256a32 32 0 0 1 32 32V192h256a32 32 0 1 1 0 64h-64v672a32 32 0 0 1-32 32H192a32 32 0 0 1-32-32zm448-64v-64H416v64zM224 896h576V256H224zm192-128a32 32 0 0 1-32-32V416a32 32 0 0 1 64 0v320a32 32 0 0 1-32 32m192 0a32 32 0 0 1-32-32V416a32 32 0 0 1 64 0v320a32 32 0 0 1-32 32"
                    ></path>
                  </svg>
                </div>
              </template>
              <!-- 选中/未选中切换按钮 -->
              <div class="he-control-btn heimgfont">
                <svg
                  @click="toggleCheckStatus"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 1024 1024"
                >
                  <!-- 选中状态图标 -->
                  <path
                    v-if="dataList[nowImgIndex]?.checkStatus"
                    fill="currentColor"
                    d="M512 64a448 448 0 1 1 0 896 448 448 0 0 1 0-896m0 393.664L407.936 353.6a38.4 38.4 0 1 0-54.336 54.336L457.664 512 353.6 616.064a38.4 38.4 0 1 0 54.336 54.336L512 566.336 616.064 670.4a38.4 38.4 0 1 0 54.336-54.336L566.336 512 670.4 407.936a38.4 38.4 0 1 0-54.336-54.336z"
                  ></path>
                  <!-- 未选中状态图标 -->
                  <path
                    v-else
                    fill="currentColor"
                    d="M512 64a448 448 0 1 1 0 896 448 448 0 0 1 0-896m-55.808 536.384-99.52-99.584a38.4 38.4 0 1 0-54.336 54.336l126.72 126.72a38.272 38.272 0 0 0 54.336 0l262.4-262.464a38.4 38.4 0 1 0-54.272-54.336z"
                  ></path>
                </svg>
              </div>
            </template>
          </div>
        </div>
        <!-- 页码指示器 -->
        <div class="he-control-num" v-if="controlBar && multiple">
          {{ imgIndex + 1 }} / {{ imgList.length }}
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "hevue-img-preview",
  data() {
    return {
      // imgWidth: 0,
      // imgHeight: 0,

      imgScale: 1,
      imgTop: 0,
      imgLeft: 0,
      imgRotate: 0,
      isFull: false,
      maxWH: "max-width:100%;max-height:100%;",
      clientX: 0,
      clientY: 0,
      imgIndex: 0,
      canRun: true,
      imgurl: "",
      imgState: 1,
      start: [{}, {}],
      mobileScale: 0, // 手指离开时图片的缩放比例
      // 以下内容为用户传入配置
      // show: true, // 插件显示，默认为false
      url: "", // 预览图片的地址
      nowImgIndex: 0,
      multiple: false,
      imgList: [],
      // 以下为可全局配置
      controlBar: true,
      closeBtn: true,
      arrowBtn: true,
      keyboard: true,
      clickMaskCLose: false, // 是否点击遮罩关闭，默认false
      closeFn: null, // 关闭回调函数
      changeFn: null, // 切换图片回调函数
    };
  },
  mounted() {
    this.initImg();
    // 将自动切换方法暴露到全局，供外部调用
    window.triggerImgPreviewNext = this.autoNextAfterUpload;
  },
  beforeUnmount() {
    // 移除全局方法
    delete window.triggerImgPreviewNext;
  },
  watch: {
    url() {
      this.initImg();
    },
    "$store.state.imgPreview.visible": {
      handler(newV) {
        if (newV) {
          this.$nextTick(() => {
            let _dom = document.getElementById("hevue-imgpreview-wrap");
            _dom.onmousewheel = this.scrollFunc;
            // 火狐浏览器没有onmousewheel事件，用DOMMouseScroll代替(滚轮事件)
            document.body.addEventListener("DOMMouseScroll", this.scrollFunc);
            // 禁止火狐浏览器下拖拽图片的默认事件
            document.ondragstart = function () {
              return false;
            };
            // 判断是否多图
            if (this.multiple) {
              if (Array.isArray(this.imgList) && this.imgList.length > 0) {
                this.imgIndex = Number(this.nowImgIndex) || 0;
                // this.url = this.imgList[this.imgIndex]
                this.changeUrl(this.imgList[this.imgIndex], this.imgIndex);
              } else {
                // console.error("imgList 为空或格式不正确");
              }
            } else {
              this.changeUrl(this.url);
            }
            // 判断是否开启键盘事件
            if (this.keyboard) {
              document.addEventListener("keydown", this.keyHandleDebounce);
            }
          });
        }
      },
      immediate: true,
    },
  },
  methods: {
    show() {
      this.$store.commit("SET_VISIBLE", true);
    },
    close(data) {
      this.initImg();
      // this.maxWH = "max-width:100%;max-height:100%;";
      // this.isFull = false;
      // 移除火狐浏览器下的鼠标滚动事件
      document.body.removeEventListener("DOMMouseScroll", this.scrollFunc);
      //恢复火狐及Safari浏览器下的图片拖拽
      document.ondragstart = null;
      // 移除键盘事件
      if (this.keyboard) {
        document.removeEventListener("keydown", this.keyHandleDebounce);
      }
      this.$store.commit("SET_VISIBLE", false);
      this.closeFn && this.closeFn(data);
    },
    initImg() {
      this.mobileScale = 1;
      this.imgScale = 1;
      this.imgRotate = 0;
      this.imgTop = 0;
      this.imgLeft = 0;
    },
    /**
     * 切换图片
     * true 下一张
     * false 上一张
     */
    toogleImg(bool, way) {
      let fromIndex = this.imgIndex;
      if (bool) {
        this.nowImgIndex++;
        this.imgIndex++;

        if (this.imgIndex > this.imgList.length - 1) {
          this.imgIndex = 0;
          this.nowImgIndex = 0;
        }
      } else {
        this.nowImgIndex--;
        this.imgIndex--;
        if (this.imgIndex < 0) {
          this.imgIndex = this.imgList.length - 1;
          this.nowImgIndex = this.nowImgIndex.length - 1;
        }
      }
      this.changeFn &&
        this.changeFn({
          type: bool ? "next" : "prev",
          fromImgIndex: fromIndex,
          fromImgUrl: this.imgList[fromIndex],
          toImgIndex: this.imgIndex,
          toImgUrl: this.imgList[this.imgIndex],
          way,
        });
      // this.url = this.imgList[this.imgIndex]
      this.changeUrl(this.imgList[this.imgIndex], this.imgIndex);
    },
    // 改变图片地址
    /**
     * @description:
     * @param {String} url 要显示的图片的url
     * @param {Number} index 当前显示当图片下标，防止用户点击切换图片过快
     * @return {*}
     */
    changeUrl(url, index) {
      this.imgState = 1;
      let img = new Image();
      img.src = url;
      img.onload = () => {
        // 如果加载出来图片当下标不是当前显示图片当下标，则不予显示（用户点击过快当时候，会出现用户点到第三张了，此时第一张图片才加载完当情况）
        if (index != undefined && index == this.imgIndex) {
          this.imgState = 2;
          this.imgurl = url;
        } else if (index == undefined) {
          this.imgState = 2;
          this.imgurl = url;
        }
      };
      img.onerror = () => {
        if (index != undefined && index == this.imgIndex) {
          this.imgState = 3;
        } else if (index == undefined) {
          this.imgState = 3;
        }
      };
    },
    // 旋转图片
    rotateFunc(deg) {
      this.imgRotate += deg;
    },
    // 图片缩放
    scaleFunc(num, bool) {
      if (this.imgScale <= 0.2 && num < 0) return;
      if (bool) {
        this.imgScale = num;
      } else {
        this.imgScale += num;
      }
    },
    // 图片原尺寸切换
    imgToggle() {
      this.initImg();
      if (this.isFull) {
        this.maxWH = "max-width:100%;max-height:100%;";
      } else {
        this.maxWH = "";
      }
      this.isFull = !this.isFull;
    },
    // 鼠标滚轮缩放
    scrollFunc(e) {
      e = e || window.event;
      // e.returnValue = false // ie
      // 火狐下没有wheelDelta，用detail代替，由于detail值的正负和wheelDelta相反，所以取反
      e.delta = e.wheelDelta || -e.detail;

      e.preventDefault();
      if (e.delta > 0) {
        //当滑轮向上滚动时
        this.scaleFunc(0.05);
      }
      if (e.delta < 0) {
        //当滑轮向下滚动时
        this.scaleFunc(-0.05);
      }
    },
    // 鼠标按下
    addMove(e) {
      e = e || window.event;
      this.clientX = e.clientX;
      this.clientY = e.clientY;
      this.$refs.heImg.onmousemove = this.moveFunc;
    },
    // 手指按下事件
    addMoveMobile(e) {
      e.preventDefault();
      e = e || window.event;
      if (e.touches.length > 1) {
        this.start = e.touches;
      } else {
        this.clientX = e.touches[0].pageX;
        this.clientY = e.touches[0].pageY;
      }
      // 添加手指拖动事件
      this.$refs.heImg.ontouchmove = this.moveFuncMobile;
    },
    // 鼠标拖动
    moveFunc(e) {
      e = e || window.event;
      e.preventDefault();
      let movementX = e.clientX - this.clientX;
      let movementY = e.clientY - this.clientY;
      // event.clientY;
      this.imgLeft += movementX * 2;
      this.imgTop += movementY * 2;
      this.clientX = e.clientX;
      this.clientY = e.clientY;
    },
    // 手指拖动
    moveFuncMobile(e) {
      e = e || window.event;
      if (e.touches.length > 1) {
        var now = e.touches;
        var scale =
          this.getDistance(now[0], now[1]) /
          this.getDistance(this.start[0], this.start[1]);
        // 判断是否手指缩放过，如果缩放过，要在上次缩放的比例基础上进行缩放
        if (this.mobileScale) {
          if (scale > 1) {
            // 放大
            this.scaleFunc(scale + this.mobileScale - 1, true);
          } else {
            // 缩小
            this.scaleFunc(scale * this.mobileScale, true);
          }
        } else {
          this.scaleFunc(scale, true);
        }
      } else {
        let touch = e.touches[0];
        e.preventDefault();
        let movementX = touch.pageX - this.clientX;
        let movementY = touch.pageY - this.clientY;
        // event.clientY;
        this.imgLeft += movementX * 2;
        this.imgTop += movementY * 2;
        this.clientX = touch.pageX;
        this.clientY = touch.pageY;
      }
    },
    // 移除拖动事件
    removeMove(type) {
      if (type === "pc") {
        this.$refs.heImg.onmousemove = null;
      } else {
        this.mobileScale = this.imgScale;
        this.$refs.heImg.ontouchmove = null;
      }
    },
    keyHandleDebounce(e) {
      if (this.canRun) {
        // 如果this.canRun为true证明当前可以执行函数
        this.keyHandle(e);
        this.canRun = false; // 执行函数后一段时间内不可再次执行
        setTimeout(() => {
          this.canRun = true; // 等到了我们设定的时间之后，把this.canRun改为true，可以再次执行函数
        }, 300);
      }
    },
    // 键盘事件
    keyHandle(e) {
      e = window.event || e;
      var key = e.keyCode || e.which || e.charCode;
      switch (key) {
        case 27: // esc
          this.close({ way: "esc" });
          break;
        case 65: // a键-上一张
          if (this.multiple) {
            this.toogleImg(false, "key-a");
          }
          break;
        case 68: // d键-下一张
          if (this.multiple) {
            this.toogleImg(true, "key-d");
          }
          break;
        case 87: // w键-放大
          this.scaleFunc(0.15);
          break;
        case 83: // s键-缩小
          this.scaleFunc(-0.15);
          break;
        case 81: // q键-逆时针旋转
          this.rotateFunc(-90);
          break;
        case 69: // e键-顺时针旋转
          this.rotateFunc(90);
          break;
        case 82: // r键-复位键
          this.initImg();
          break;

        default:
          break;
      }
    },
    // 点击遮罩层
    clickMask() {
      if (this.clickMaskCLose) {
        this.close({ way: "mask" });
      }
    },
    //缩放 勾股定理方法-求两点之间的距离
    getDistance(p1, p2) {
      var x = p2.pageX - p1.pageX,
        y = p2.pageY - p1.pageY;
      return Math.sqrt(x * x + y * y);
    },
    /**
     * @description:
     * @param {String} imgsrc
     * @param {*} name
     * @return {*}
     */
    downloadIamge() {
      //下载图片地址和图片名
      let image = new Image();
      // 解决跨域 Canvas 污染问题
      image.setAttribute("crossOrigin", "anonymous");
      image.onload = function () {
        let canvas = document.createElement("canvas");
        canvas.width = image.width;
        canvas.height = image.height;
        let context = canvas.getContext("2d");
        context.drawImage(image, 0, 0, image.width, image.height);
        let url = canvas.toDataURL("image/png"); //得到图片的base64编码数据
        let a = document.createElement("a"); // 生成一个a元素
        let event = new MouseEvent("click"); // 创建一个单击事件
        a.download = "photo" + +new Date(); // 设置图片名称
        a.href = url; // 将生成的URL设置为a.href属性
        a.dispatchEvent(event); // 触发a的单击事件
      };
      image.onerror = function (err) {
        console.log("图片信息不正确或图片服务器禁止访问");
        console.log(err);
      };
      if (this.multiple) {
        image.src = this.imgList[this.imgIndex];
      } else {
        image.src = this.url;
      }
    },
    customUpload() {
      // 如果传入了 onupload 回调函数，则调用它
      if (this.onupload) {
        this.onupload({ dataUrl: this.dataList[this.nowImgIndex] });
      }
    },
    // 新增：上传成功后的回调方法
    triggerUploadSuccess(data) {
      // 如果传入了 onUploadSuccess 回调函数，则调用它
      if (this.onUploadSuccess) {
        this.onUploadSuccess(data);
      }

      // 上传成功后自动切换到下一张图片（如果不是最后一张）
      this.autoNextAfterUpload();
    },
    // 新增：上传成功后自动切换到下一张图片
    autoNextAfterUpload() {
      // 重新获取最新的图片列表，确保与外部数据同步
      if (this.dataList && this.dataList.length > 0) {
        // 从 dataList 中重新构建 imgList
        this.imgList = this.dataList.map(
          (item) => item.image_url || item.url || item
        );
      }

      // 检查是否还有下一张图片
      if (this.multiple && this.imgIndex < this.imgList.length - 1) {
        // 不是最后一张，切换到下一张
        this.toogleImg(true, "upload-success");
      } else if (this.multiple && this.imgIndex >= this.imgList.length - 1) {
        // 是最后一张，可以选择关闭预览
        this.$store.commit("SET_VISIBLE", false);
      }
    },
    // 自定义删除方法
    customDelete() {
      // 如果传入了 ondelete 回调函数，则调用它
      if (this.ondelete) {
        this.ondelete({ dataUrl: this.dataList[this.nowImgIndex] });
      }
    },
    // 切换选中状态
    toggleCheckStatus() {
      if (this.dataList[this.nowImgIndex]) {
        this.dataList[this.nowImgIndex].checkStatus =
          !this.dataList[this.nowImgIndex].checkStatus;
        if (this.multiple && this.imgIndex < this.imgList.length - 1) {
          this.toogleImg(true, "upload-success");
        }
      }
    },
  },
};
</script>

<style scoped>
@import "./iconfont/iconfont.css";
@import "./css/default.css";
</style>
