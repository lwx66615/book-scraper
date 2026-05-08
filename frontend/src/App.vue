<template>
  <el-container class="app-container">
    <el-header>
      <div class="header-content">
        <h1>网络小说爬虫</h1>
        <el-menu mode="horizontal" :default-active="activeMenu" router>
          <el-menu-item index="/">书架</el-menu-item>
          <el-menu-item index="/download">下载中心</el-menu-item>
          <el-menu-item index="/rules">规则配置</el-menu-item>
          <el-menu-item index="/settings">设置</el-menu-item>
        </el-menu>
      </div>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app-container {
  min-height: 100vh;
}

.el-header {
  background-color: #409eff;
  color: white;
}

.header-content {
  display: flex;
  align-items: center;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.header-content h1 {
  margin-right: 40px;
  font-size: 20px;
}

.el-menu--horizontal {
  background-color: transparent;
  border-bottom: none;
}

.el-menu--horizontal .el-menu-item {
  color: white;
  border-bottom: none;
}

.el-menu--horizontal .el-menu-item:hover,
.el-menu--horizontal .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.2);
  border-bottom: none;
}
</style>
