<template>
  <div class="facedetectionBox">
    <div class="face-formbox">
      <div class="face-title">验证表单</div>
      <div class="face-top">
        <div class="face-top-left">
          <div class="selectimage">
            <div class="selectimage-imgbox">
              <div
                v-if="imageurl == null"
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
            <el-form-item label="Id" prop="id">
              <el-input v-model="ruleForm.id" />
            </el-form-item>
            <el-form-item label="类型" prop="type">
              <el-input v-model="ruleForm.type" />
            </el-form-item>
            <el-form-item label="Dob" prop="dob">
              <el-input v-model="ruleForm.dob" />
            </el-form-item>
            <el-form-item label="Pob" prop="pob">
              <el-input v-model="ruleForm.pob" />
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
            :disabled="imageurl == null"
            :loading="isThrottled"
            >提交</el-button
          >
        </div>
      </div>
    </div>
    <div class="face-result">
      <div class="face-title">检测结果</div>
      <div class="result-textbox" v-if="resultData">
        <div v-html="resultData"></div>
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
import { ImageAnalyze } from "@/api/api";
export default {
  data() {
    return {
      imageurl: null,
      ruleForm: { name: "", id: "", type: "", dob: "", pob: "" },
      rules: {
        type: [{ required: true, message: "请输入type", trigger: "blur" }],
      },
      resultData: null,
      isThrottled: false,
    };
  },
  methods: {
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
          // 设置1.5秒后解除节流状态
          setTimeout(() => {
            this.isThrottled = false;
          }, 1500);
          ImageAnalyze({
            img: this.imageurl,
            type: this.ruleForm.type,
            id: this.ruleForm.id,
            name: this.ruleForm.name,
            dob: this.ruleForm.dob,
            pob: this.ruleForm.pob,
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
      this.imageurl = null;
      this.resultData = null;
      this.ruleForm = { name: "", id: "", type: "", dob: "", pob: "" };
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
            }

            .Faceimage:hover {
              .el-icon-delete {
                visibility: visible;
                // z-index: 100;
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
    }
  }
  #notReplicable {
    cursor: pointer;
    user-select: none;
  }
}
</style>