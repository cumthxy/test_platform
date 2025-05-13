<template>
  <div class="facedetectionBox">
    <div class="face-formbox">
      <div class="face-title"></div>
      <div class="face-top">
        <div class="face-top-left">
          <div class="selectimage">
            <div class="selectimage-imgbox">
              <div v-if="!imageurl" id="notReplicable" class="uploadimg">
                <span>+</span>
                <img src="../../../public/头像.png" alt="" />
                <span>图片</span>
                <input
                  id="fileInput"
                  type="file"
                  ref="uploadimg"
                  accept="image/png,image/jpeg,image/ipg,image"
                  name="uploadinput"
                  @change="checkFile($event)"
                />
              </div>
              <div v-else class="Faceimage">
                <el-image
                  :src="imageurl"
                  fit="contain"
                  :preview-src-list="ImgList"
                >
                </el-image>
                <el-icon @click="imageurl = ''"><Delete /></el-icon>
              </div>
            </div>
            <div class="tips">
              <div>支持的文件:</div>
              <ul>
                <li>* PNG和JPEG图像.</li>
                <li>* 像素尺寸大于128x128的图像.</li>
                <li>* 小于2MB的文件.</li>
              </ul>
            </div>
          </div>
          <div class="md5download">
            <div class="md5-title">MD5图片下载</div>
            <el-form
              ref="md5Form"
              :model="md5Form"
              :rules="md5rules"
              :inline="true"
            >
              <el-form-item label="Img_md5" prop="img_md5">
                <el-input
                  v-model="md5Form.img_md5"
                  placeholder="请输入img_md5"
                  style="width: 250px"
                />
              </el-form-item>
              <el-form-item label="Md5_type" prop="md5_type">
                <el-select
                  v-model="md5Form.md5_type"
                  filterable
                  placeholder="请选择md5_type"
                  style="width: 250px"
                >
                  <el-option
                    v-for="(item, index) in options"
                    :key="item.value + index"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </el-form-item>
            </el-form>
            <div class="download-btn">
              <el-button
                size="small"
                type="primary"
                @click="downloadMd5Img"
                :loading="isLoading"
                >下载</el-button
              >
            </div>
          </div>
        </div>
        <div class="face-top-right">
          <el-form
            ref="alertForm"
            style="max-width: 600px"
            :model="ruleForm"
            :rules="rules"
            label-width="auto"
            class="demo-ruleForm"
            status-icon
          >
            <el-form-item label="姓名" prop="name">
              <el-input v-model="ruleForm.name" placeholder="请输入姓名" />
            </el-form-item>
            <el-form-item label="证件号" prop="id">
              <el-input v-model="ruleForm.id" placeholder="请输入证件号" />
            </el-form-item>
            <el-form-item label="电话" prop="phone">
              <el-input v-model="ruleForm.phone" placeholder="请输入电话" />
            </el-form-item>
            <el-form-item label="类型" prop="type">
              <el-select
                v-model="ruleForm.type"
                filterable
                placeholder="请输入类型关键词"
                @change="handleSelect"
              >
                <el-option
                  v-for="(item, index) in suggestions"
                  :key="item.value + index"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="Dob" prop="dob">
              <el-input v-model="ruleForm.dob" placeholder="请输入出生日期" />
            </el-form-item>
            <el-form-item label="Pob" prop="pob">
              <el-input v-model="ruleForm.pob" placeholder="请输入出生地" />
            </el-form-item>
            <el-form-item label="国家码(大写)" prop="country">
              <el-input v-model="ruleForm.country" placeholder="请输入国家码" />
            </el-form-item>
          </el-form>
        </div>
      </div>
      <div class="face-bottom">
        <div class="buttonbox">
          <el-button size="small" @click="reset">重置</el-button>
          <el-button
            size="small"
            type="primary"
            @click="submit"
            :loading="isThrottled"
            >提交</el-button
          >
        </div>
      </div>
    </div>
    <div class="face-result" v-loading="isThrottled">
      <div class="face-title">检测结果</div>
      <div class="result-textbox" v-if="resultData">
        <pre class="preformatted-text">{{ formattedResult }}</pre>
      </div>
      <div v-else>
        <el-empty :image-size="130" />
      </div>
    </div>
  </div>
</template>

<script>
import { ImageAnalyze, getanalyzeType, getMd5Type, downMd5 } from "@/api/api";
export default {
  data() {
    return {
      imageurl: "",
      ImgList: [],
      md5Form: {
        img_md5: "",
        md5_type: "",
      },
      md5rules: {
        img_md5: [
          { required: true, message: "请输入img_md5", trigger: "blur" },
        ],
        md5_type: [
          { required: true, message: "请输入md5_type", trigger: "blur" },
        ],
      },
      ruleForm: {
        name: "",
        id: "",
        phone: "",
        pe: "",
        dob: "",
        pob: "",
        country: "",
      },
      rules: {
        type: [{ required: true, message: "请输入type", trigger: "blur" }],
      },
 
      resultData: null,
      isThrottled: false,
      isLoading: false,
      options: [],
      suggestions: [],
    };
  },  
  methods: {
    handleSelect(value) {
      // 通过 value 在 suggestions 中查找对应对象
      const selected = this.suggestions.find(item => item.value === value);
      if (selected) {
        this.ruleForm.type = selected.value;
        this.ruleForm.api_id = selected.api_id;
      }
    },

    checkFile(e) {
      const _fileObj = e.target.files[0];
      // 尺寸大小报错
      if (_fileObj && _fileObj.size > 2 * 1024 * 1024) {
        this.$message.warning("Picture size exceeds 2MB！");
      } else {
        // 转为base64格式进行渲染
        const reader = new FileReader();
        reader.readAsDataURL(_fileObj);
        reader.onload = (e) => {
          this.imageurl = e.target.result;
          this.ImgList[0] = this.imageurl;
        };
      }
    },

    submit() {
      this.$refs.alertForm.validate(async (valid) => {
        if (valid) {
          if (this.isThrottled) {
            return;
          }
          // 设置节流状态为true
          this.isThrottled = true;
          try {
            let imageRes = await ImageAnalyze({
              img: this.imageurl,
              type: this.ruleForm.type,
              api_id: this.ruleForm.api_id,
              id: this.ruleForm.id,
              phone: this.ruleForm.phone,
              name: this.ruleForm.name,
              dob: this.ruleForm.dob,
              pob: this.ruleForm.pob,
              country: this.ruleForm.country,
            });
            if (imageRes.re_code == 200) {
              this.isThrottled = false;
              this.resultData = JSON.stringify(imageRes.msg);
            } else {
              this.isThrottled = false;
            }
          } catch (error) {
            this.isThrottled = false;
          }
        }
      });
    },
    reset() {
      this.imageurl = "";
      this.resultData = null;
      this.ruleForm = {
        name: "",
        id: "",
        phone: "",
        pe: "",
        dob: "",
        pob: "",
        country: "",
      };
    },
    downloadMd5Img() {
      this.$refs.md5Form.validate(async (valid) => {
        if (valid) {
          if (this.isLoading) {
            return;
          }
          // 设置节流状态为true
          this.isLoading = true;
          let res = await downMd5({
            img_md5: this.md5Form.img_md5,
            md5_type: this.md5Form.md5_type,
          });
          if (res.re_code === 200) {
            // 创建一个临时的 a 标签用于下载
            const link = document.createElement("a");
            link.href = res.msg;
            // 从 URL 中提取文件名，如果没有则使用默认名称
            const fileName = res.msg.split("/").pop() || "download";
            link.download = fileName;
            // 添加到文档中
            document.body.appendChild(link);
            // 触发点击
            link.click();
            // 清理 DOM
            document.body.removeChild(link);
            this.$message.success("下载成功");
          }
          this.isLoading = false;
        }
      });
    },
  },
  computed: {
    formattedResult() {
      const data =
        typeof this.resultData === "string"
          ? JSON.parse(this.resultData)
          : this.resultData;

      // 格式化 JSON
      return data ? JSON.stringify(data, null, 2) : "";
    },
  },
  async mounted() {
    try {
      const response = await getanalyzeType({});
      if (response?.re_code === 200 && Array.isArray(response.msg)) {
        this.suggestions = response.msg.map((item) => ({
          value: item.name, // 显示的值
          api_id: item.api_id,
        })); // 存储结果到本地变量
      }
    } catch (error) {}

    getMd5Type().then((res) => {
      if (res.re_code == 200) {
        this.options = res.msg.map((item) => {
          return {
            value: item,
            label: item,
          };
        });
      }
    });
  },
};
</script>

<style lang="scss" scoped>
.facedetectionBox {
  display: flex;
  flex-direction: column;
  .face-title {
    border-bottom: 1px solid #e4e7ed;
    padding: 20px;
  }
  .face-formbox {
    border-radius: 4px;
    box-sizing: border-box;
    background-color: #fff;
    box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.12);
    .face-top {
      display: flex;
      padding: 20px;
      .face-top-left {
        width: 55%;
        border-right: 1px solid #e4e7ed;
        .selectimage {
          width: 100%;
          display: flex;
          box-sizing: border-box;
          align-items: flex-start;
          .selectimage-imgbox {
            width: 400px;
            height: 176px;
            display: flex;
            align-items: center;
            .uploadimg {
              width: 400px;
              height: 176px;
              border: 1px dashed #1890ff;
              box-sizing: border-box;
              position: relative;
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: space-evenly;

              > span:nth-child(1) {
                position: absolute;
                top: -6px;
                right: 8px;
                color: #1890ff;
                font-size: 25px;
              }

              > span:nth-child(2) {
                display: block;
                height: 72px;
                width: 72px;
                border-radius: 72px;
                background-color: #e5f1fc;
              }

              > span:nth-child(3) {
                font-size: 14px;
                font-family: PingFangSC-Semibold, PingFang SC;
                font-weight: 600;
                color: #1890ff;
              }

              input {
                width: 100%;
                height: 100%;
                opacity: 0;
                position: absolute;
                left: 0;
                top: 0;
                cursor: pointer;
              }
            }

            > span {
              width: 39px;
              height: 25px;
              font-size: 18px;
              font-family: PingFangSC-Semibold, PingFang SC;
              font-weight: 600;
              color: #1890ff;
              line-height: 25px;
              margin: 0 24px;
            }

            .Faceimage {
              width: 400px;
              height: 176px;
              background: rgba(247, 247, 247, 0);
              box-shadow: 0px 0px 3px 0px rgba(0, 0, 0, 0.25);
              border: 1px solid #e9e9e9;
              border-radius: 2px;
              display: flex;
              align-items: center;
              position: relative;
              .el-image {
                width: 100%;
                height: 100%;
                img {
                  width: 100%;
                  height: 100%;
                  user-select: none;
                  -webkit-user-drag: none;
                }
              }
              .el-icon {
                cursor: pointer;
                position: absolute;
                visibility: hidden;
                color: red;
                top: 5px;
                right: 10px;
              }
            }

            .Faceimage:hover {
              .el-icon {
                visibility: visible;
              }
            }
          }

          .tips {
            width: 315px;
            height: 80px;
            padding-top: 8px;
            padding-left: 30px;
            display: flex;
            flex-direction: column;
            align-items: flex-start;

            div {
              font-size: 12px;
              font-family: PingFangSC-Semibold, PingFang SC;
              font-weight: 600;
              color: rgba(0, 0, 0, 0.65);
              margin-bottom: 4px;
            }

            ul {
              display: flex;
              flex-direction: column;
              align-items: flex-start;

              li {
                font-size: 10px;
                font-family: PingFangSC-Regular, PingFang SC;
                font-weight: 400;
                color: rgba(0, 0, 0, 0.65);
                line-height: 16px;
              }
            }
          }
        }
        .md5download {
          margin-top: 20px;
          display: flex;
          flex-direction: column;
          border-radius: 4px;
          padding: 20px;

          .md5-title {
            font-size: 16px;
            font-weight: 600;
            color: #303133;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e4e7ed;
          }

          :deep(.el-form) {
            .el-form-item {
              margin-right: 20px;
              margin-bottom: 0;
            }
          }

          .download-btn {
            display: flex;
            justify-content: flex-end;
            margin-top: 15px;
            padding: 0 20px;
            .el-button--small {
              padding: 8px 14px;
              border-radius: 6px;
            }
          }
        }
      }
      .face-top-right {
        width: 45%;
        padding-left: 30px;
      }
    }
    .face-bottom {
      display: flex;
      align-items: flex-end;
      justify-content: flex-end;
      padding: 0 20px 20px 20px;

      .buttonbox {
        .el-button--small {
          padding: 8px 14px;
          border-radius: 6px;
        }

        .el-button--primary {
          margin-left: 16px;
        }
      }
    }
  }
  .face-result {
    margin: 20px 0;
    border-radius: 4px;
    box-sizing: border-box;
    background-color: #fff;
    box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.12);
    .result-textbox {
      padding: 20px !important;
      max-width: 100%; /* 可选：设置容器的最大宽度 */
      word-wrap: break-word; /* 强制内容换行 */
      white-space: pre-wrap; /* 保留空格和换行符 */
      .preformatted-text {
        font-family: monospace; /* 使用等宽字体 */
        white-space: pre-wrap; /* 保留空格和换行 */
        word-wrap: break-word; /* 长内容自动换行 */
        background-color: #f5f5f5; /* 可选：添加代码块的背景色 */
        padding: 10px; /* 可选：设置内边距 */
        border-radius: 5px; /* 可选：设置圆角 */
        border: 1px solid #ddd; /* 可选：设置边框 */
        overflow-x: auto; /* 可选：允许横向滚动 */
      }
    }
  }
  #notReplicable {
    cursor: pointer;
    user-select: none;
  }
}
</style>