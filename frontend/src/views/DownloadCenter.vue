<template>
  <div class="download-center">
    <h2>下载中心</h2>

    <div class="tasks-list" v-loading="loading">
      <TaskItem
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        @pause="handlePause"
        @resume="handleResume"
        @cancel="handleCancel"
      />

      <el-empty v-if="!loading && tasks.length === 0" description="暂无下载任务" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { downloadApi } from '../api'
import TaskItem from '../components/TaskItem.vue'

const tasks = ref([])
const loading = ref(false)
let pollTimer = null

const loadTasks = async () => {
  try {
    const data = await downloadApi.getTasks()
    tasks.value = data.items
  } catch (error) {
    console.error('加载任务失败:', error)
  }
}

const handlePause = async (taskId) => {
  try {
    await downloadApi.pause(taskId)
    ElMessage.success('已暂停')
    await loadTasks()
  } catch (error) {
    ElMessage.error(error.message)
  }
}

const handleResume = async (taskId) => {
  try {
    await downloadApi.resume(taskId)
    ElMessage.success('已继续')
    await loadTasks()
  } catch (error) {
    ElMessage.error(error.message)
  }
}

const handleCancel = async (taskId) => {
  try {
    await ElMessageBox.confirm('确定要取消这个下载任务吗？', '提示', {
      type: 'warning'
    })
    await downloadApi.cancel(taskId)
    ElMessage.success('已取消')
    await loadTasks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message)
    }
  }
}

onMounted(() => {
  loadTasks()
  // 每3秒轮询更新任务状态
  pollTimer = setInterval(loadTasks, 3000)
})

onUnmounted(() => {
  if (pollTimer) {
    clearInterval(pollTimer)
  }
})
</script>

<style scoped>
.download-center {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.download-center h2 {
  margin-bottom: 20px;
}

.tasks-list {
  min-height: 200px;
}
</style>
