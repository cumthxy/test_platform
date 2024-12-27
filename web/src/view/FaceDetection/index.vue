<template>
  <div class="facedetectionBox">
    <div class="face-formbox">
      <div class="face-title">验证表单</div>
      <div class="face-top">
        <div class="face-top-left">
          <div class="selectimage">
            <div class="selectimage-imgbox">
              <div
                v-if="!imageurl"
                id="notReplicable"
                class="uploadimg"
                @click="dialogVisible = true"
              >
                <span>+</span>
                <img src="../../../public/头像.png" alt="" />
                <span>人脸</span>
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
                <el-image :src="imageurl" fit="contain"> </el-image>
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
              <el-input v-model="ruleForm.name" />
            </el-form-item>
            <el-form-item label="证件号" prop="id">
              <el-input v-model="ruleForm.id" />
            </el-form-item>
            <el-form-item label="电话" prop="phone">
              <el-input v-model="ruleForm.phone" />
            </el-form-item>
            <el-form-item label="类型" prop="type">
              <el-autocomplete
                v-model="ruleForm.type"
                :fetch-suggestions="querySearchType"
                @select="handleSelect"
                placeholder="请输入类型关键词"
              />
            </el-form-item>
            <el-form-item label="Dob" prop="dob">
              <el-input v-model="ruleForm.dob" />
            </el-form-item>
            <el-form-item label="Pob" prop="pob">
              <el-input v-model="ruleForm.pob" />
            </el-form-item>
            <el-form-item label="国家码(大写)" prop="country">
              <el-input v-model="ruleForm.country" />
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
        <!-- <el-descriptions :border="true" column="1">
          <el-descriptions-item
            align="center"
            v-for="(value, key) in resultData"
            :key="key"
            :label="key"
          >
            {{ value }}
          </el-descriptions-item>
        </el-descriptions> -->
      </div>
      <div v-else>
        <el-empty :image-size="200" />
      </div>
    </div>
  </div>
</template>

<script>
import "@/style/content.min.css";
import { ImageAnalyze, getanalyzeType } from "@/api/api";
export default {
  data() {
    return {
      imageurl: "",
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
      suggestions: [],
      resultData: null,
      isThrottled: false,
    };
  },
  methods: {
    async querySearchType(queryString, cb) {
      if (!queryString) {
        cb([]); // 如果输入为空，返回空数组
        return;
      }

      try {
        const response = await getanalyzeType({ type: queryString });

        if (response?.re_code === 200 && Array.isArray(response.msg)) {
          this.suggestions = response.msg.map((item) => ({
            value: item.name, // 显示的值
            api_id: item.api_id,
          })); // 存储结果到本地变量

          cb(this.suggestions); // 回调设置为搜索结果
        } else {
          cb([]); // 如果接口返回异常，返回空数组
        }
      } catch (error) {
        console.error("Error fetching suggestions:", error);
        cb([]); // 如果请求失败，返回空数组
      }
    },
    // 选择下拉框中的某一项
    handleSelect(item) {
      this.ruleForm.type = item.value; // 更新输入框的值
      this.ruleForm.api_id = item.api_id; // 更新输入框的值
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
        };
      }
    },

    submit() {
      this.$refs.alertForm.validate((valid) => {
        if (valid) {
          if (this.isThrottled) {
            return;
          }
          // 设置节流状态为true
          this.isThrottled = true;

          ImageAnalyze({
            img: this.imageurl,
            type: this.ruleForm.type,
            api_id: this.ruleForm.api_id,
            id: this.ruleForm.id,
            phone: this.ruleForm.phone,
            name: this.ruleForm.name,
            dob: this.ruleForm.dob,
            pob: this.ruleForm.pob,
            country: this.ruleForm.country,
          }).then((res) => {
            console.log(res);
            if (res.re_code == 200) {
              this.isThrottled = false;
              this.resultData = JSON.stringify(res.msg);
            }
          });
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
        width: 50%;
        border-right: 1px solid #e4e7ed;
        .selectimage {
          width: 100%;
          height: 100%;
          display: flex;
          box-sizing: border-box;
          align-items: flex-start;
          flex-direction: column;
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
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            justify-content: flex-end;

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
      }
      .face-top-right {
        width: 50%;
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
    min-height: 400px;
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