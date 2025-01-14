
<template>
  <div class="login-wrap">
    <el-form
      :model="ruleForm"
      status-icon
      :rules="rules"
      ref="ruleForm"
      class="login-container"
    >
      <h1 class="title">测试评估平台</h1>
      <el-form-item prop="username">
        <el-input
          type="text"
          v-model="ruleForm.username"
          placeholder="user name"
          autocomplete="off"
        >
          <template #prefix>
            <el-icon class="el-input__icon"><User /></el-icon> </template
        ></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          type="password"
          v-model="ruleForm.password"
          placeholder="pass word"
          autocomplete="off"
          show-password
        >
          <template #prefix>
            <el-icon class="el-input__icon"><Lock /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item>
        <el-button
          type="primary"
          @click="doLogin"
          style="width: 100%"
          :loading="status"
          >login</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>
 
<script>
import { login } from "../../api/api";
export default {
  name: "Login",
  data: function () {
    return {
      //登陆按钮显示状态
      status: false,
      ruleForm: {
        username: "",
        password: "",
      },
      rules: {
        username: [
          {
            required: true,
            message: "Please input a  user name",
            trigger: "blur",
          },
        ],
        password: [
          {
            required: true,
            message: "Please input a password",
            trigger: "blur",
          },
        ],
      },
    };
  },
  methods: {
    //登陆
    doLogin() {
      this.$refs.ruleForm.validate(async (valid) => {
        if (valid) {
          this.status = true;
          let loginres = await login({
            user_name: this.ruleForm.username,
            password: this.ruleForm.password,
          });
          if (loginres.re_code == 200) {
            localStorage.setItem("token", JSON.stringify(loginres.token));
          this.$router.push("/layout");
          }
          this.status = false;

        } else {
          this.status = false;

          this.$message({
            message: "Please check the input content",
            type: "error",
          });
          return false;
        }
      });
    },
  },
  mounted() {
    localStorage.removeItem("token");
  },
};
</script>
 
<style lang="scss">
.login-wrap {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  padding-top: 15%;
  background-image: url("../../../public/bj.svg");
  background-position: center right;
  background-size: 100%;
}

.login-container {
  border-radius: 10px;
  margin: 0px auto;
  width: 350px;
  padding: 30px 35px 15px 35px;
  background: #fff;
  border: 1px solid #eaeaea;
  text-align: left;
  box-shadow: 0 0 20px 2px rgba(0, 0, 0, 0.1);
  .title {
    margin: 0px auto 40px auto;
    text-align: center;
    color: #505458;
  }
  .checking {
    width: 350px;
    display: flex;
    flex-direction: column;
    .el-form-item__content {
      display: flex;
      // align-items: center;

      div:nth-child(2) {
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 5px;
        width: 95px;
        height: 38px;
        margin-left: 5px;
        .captcha {
          width: 95px;
          height: 100%;
        }
      }
    }
  }
  .imgbox {
    cursor: pointer;
  }
}
</style>
