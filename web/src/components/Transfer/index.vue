<template>
    <div class="transferBox" :class="type == 'small' ? 'smallTransferBox' : null">
      <div class="transferTitle" v-if="transferText">{{ transferText }}</div>
      <div
        class="transfer-right-info"
        :class="transferText ? null : 'textSeize-info'"
      >
        <span>{{ transferValue.length }} 选中接口</span>
        <el-button text  link type="primary" :disabled="disabled" @click="transferclear"
          >清空</el-button
        >
      </div>
      <el-transfer
        filterable
        filterble="true"
        filter-placeholder="搜索接口"
        :modelValue="transferValue"
        :data="maptransferData(transferData)"
        :render-content="renderItem"
        @left-check-change="leftChange"
        @right-check-change="rightChange"
      >
      </el-transfer>
    </div>
  </template>
  
  <script>
  import { CirclePlusFilled, CircleCloseFilled } from "@element-plus/icons-vue";
  export default {
    props: ["transferText", "transferValue", "transferData", "disabled", "type"],
    data() {
      return {
       
      };
    },
    methods: {
      // 渲染穿梭框的item
      renderItem(h, option) {
        const IconComponent = this.transferValue.includes(option.key)
          ? CircleCloseFilled
          : CirclePlusFilled;
  
        return h("span", [
          h("span", " " + option.label),
          h("i", { class: "el-icon" }, [h(IconComponent)]), // 根据是否选中显示不同的图标
        ]);
      },
  
      leftChange(key) {
        this.$emit("update:left", key[0]); // 发射事件，传递新增的 key
      },
      rightChange(key) {
        this.$emit("update:right", key[0]); // 发射事件，传递需要移除的 key
      },
      transferclear() {
        this.$emit("clear"); // 发射清空事件
      },
      maptransferData(transferData) {
        return transferData.map((item) => {
          return {
            key: Number(item.id),
            label: item.name,
            disabled: this.disabled,
          };
        });
      },
    },
    mounted() {
      
    },
  };
  </script>
  
  <style lang="scss" >
  .transferBox {
    // margin-left: 40px;
    position: relative;
  
    .transferTitle {
      height: 20px;
      margin-bottom: 5px;
    }
    .transferSelect {
      z-index: 100;
      position: absolute;
      width: 140px;
      height: 34px;
      left: 170px;
      top: 41px;
      .el-select__wrapper{
      height: 34px;
      }
      .el-input__inner {
        border-radius: 2px;
        height: 32px;
      }
      .el-input__icon {
        line-height: 100%;
      }
    }
    .textSeize-select {
      top: 16px !important;
    }
    .transfer-right-info {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 300px;
      position: absolute;
      z-index: 100;
      top: 48px;
      left: 345px;
    }
    .textSeize-info {
      top: 16px !important;
    }
    //  覆盖穿梭框默认样式
    .el-transfer {
      min-width: 660px;
      .el-transfer-panel {
        min-height: 500px;
        width: 330px;
      }
  
      .el-transfer-panel__empty,
      .el-transfer__buttons,
      .el-transfer-panel__header {
        display: none !important;
      }
  
      .el-transfer-panel__filter {
        width: 175px;
        .el-input__inner {
          border-radius: 2px;
        }
      }
      .el-transfer-panel__body {
        border-top: 1px solid #ebeef5;
        min-height: 500px;
        height: 100%;
        .el-checkbox__input {
          display: none;
        }
        .el-transfer-panel__list {
          height: 420px;
          overflow: scroll;
        }
      }
      .el-checkbox__label {
        > span {
          width: 90%;
          display: flex;
          align-items: center;
          justify-content: space-between;
          i {
            color: #0088ff;
          }
        }
      }
  
      .el-checkbox:last-of-type {
        margin-right: 30px;
      }
      .el-transfer-panel:nth-child(3) {
        vertical-align: top;
        .el-transfer-panel__filter {
          /* 定位到右侧面板的搜索框 */
          display: none !important;
        }
        .el-transfer-panel__body {
          border-top: 1px solid #ebeef5;
          min-height: 500px;
          .el-checkbox-group {
            margin-top: 62px;
          }
        }
        i {
          color: #ff8d9d;
        }
      }
    }
  }
  //type 为
  .smallTransferBox {
    .el-transfer {
      .el-transfer-panel {
        min-height: 400px;
      }
      .el-transfer-panel__body {
        border-top: 1px solid #ebeef5;
        min-height: 400px !important;
        height: 100%;
        .el-checkbox__input {
          display: none;
        }
        .el-transfer-panel__list {
          height: 320px;
          overflow: scroll;
        }
      }
      
    }
  }
  </style>