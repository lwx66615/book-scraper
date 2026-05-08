<template>
  <div class="settings">
    <h2>设置</h2>

    <el-card class="settings-card">
      <template #header>自动更新</template>
      <el-form label-width="120px">
        <el-form-item label="启用自动更新">
          <el-switch v-model="autoUpdate.enabled" />
        </el-form-item>
        <el-form-item label="检查时间" v-if="autoUpdate.enabled">
          <el-input v-model="autoUpdate.cron" placeholder="Cron表达式，如: 0 9 * * *" />
          <div class="hint">每天9点检查更新</div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveAutoUpdate">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="settings-card">
      <template #header>代理设置</template>
      <el-form label-width="120px">
        <el-form-item label="代理列表">
          <el-input
            v-model="proxyText"
            type="textarea"
            :rows="4"
            placeholder="每行一个代理地址，如：&#10;http://127.0.0.1:7890&#10;http://127.0.0.1:7891"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveProxy">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { settingsApi } from '../api'

const autoUpdate = ref({
  enabled: false,
  cron: '0 9 * * *'
})

const proxyText = ref('')

const loadSettings = async () => {
  try {
    const autoUpdateData = await settingsApi.getAutoUpdate()
    autoUpdate.value = autoUpdateData

    const proxyData = await settingsApi.getProxy()
    proxyText.value = proxyData.proxies.join('\n')
  } catch (error) {
    console.error('加载设置失败:', error)
  }
}

const saveAutoUpdate = async () => {
  try {
    await settingsApi.setAutoUpdate(autoUpdate.value)
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error(error.message)
  }
}

const saveProxy = async () => {
  try {
    const proxies = proxyText.value
      .split('\n')
      .map(p => p.trim())
      .filter(p => p)

    await settingsApi.setProxy({ proxies })
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error(error.message)
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.settings {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.settings-card {
  margin-bottom: 20px;
}

.hint {
  color: #999;
  font-size: 12px;
  margin-top: 4px;
}
</style>
