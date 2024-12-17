<template>
   <div id="app">
    <router-view />
  </div>
</template>

<script>
  export default {
    
  }
</script>

<style lang="scss" >
* {
  list-style: none;
  margin: 0;
  padding: 0;
  margin: 0;
  font-family: "PingFang SC", -apple-system, BlinkMacSystemFont, "Segoe UI",
    "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji",
    "Segoe UI Emoji" !important;
}

#app {
  width: 100vw;
  height: 100vh;
  display: flex;
  .el-table__inner-wrapper {
    height: 100% !important;
  }
  .el-input__inner {
    line-height: 1px;
  }
  // 客服对比度问题 （后续会删除）
  .el-select__wrapper,
  .el-input__wrapper {
    // border: 1px solid black;
    box-sizing: border-box;
  }
  .el-table--border .el-table__cell {
    border-right: none;
  }
  input[type="number"]::-webkit-inner-spin-button,
  input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  input[type="number"] {
    -moz-appearance: textfield; /* Firefox */
  }
}
.el-dialog__body {
  padding: 0px 26px 15px 20px !important;
  box-sizing: border-box;

  .footer {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
    .el-button {
      padding: 8px 15px;
    }

  }
}
</style>