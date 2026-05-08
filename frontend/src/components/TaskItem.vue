<template>
  <el-card class="task-item">
    <div class="task-content">
      <div class="task-info">
        <h4>{{ task.novel?.title || '未知小说' }}</h4>
        <p class="status">
          <el-tag :type="statusType">{{ statusText }}</el-tag>
          <span class="progress-text">
            {{ task.downloaded_chapters }} / {{ task.total_chapters }} 章
          </span>
        </p>
        <el-progress
          :percentage="progress"
          :status="progressStatus"
          :stroke-width="10"
        />
        <p class="current" v-if="task.current_chapter && task.status === 'running'">
          正在下载：{{ task.current_chapter }}
        </p>
        <p class="error" v-if="task.error_message">
          <el-icon><WarningFilled /></el-icon>
          {{ task.error_message }}
        </p>
      </div>
      <div class="task-actions">
        <el-button
          v-if="task.status === 'running'"
          type="warning"
          size="small"
          @click="$emit('pause', task.id)"
        >
          暂停
        </el-button>
        <el-button
          v-if="task.status === 'paused'"
          type="primary"
          size="small"
          @click="$emit('resume', task.id)"
        >
          继续
        </el-button>
        <el-button
          v-if="['pending', 'running', 'paused'].includes(task.status)"
          type="danger"
          size="small"
          @click="$emit('cancel', task.id)"
        >
          取消
        </el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { WarningFilled } from '@element-plus/icons-vue'

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

defineEmits(['pause', 'resume', 'cancel'])

const statusMap = {
  pending: { text: '等待中', type: 'info' },
  running: { text: '下载中', type: 'primary' },
  paused: { text: '已暂停', type: 'warning' },
  completed: { text: '已完成', type: 'success' },
  failed: { text: '失败', type: 'danger' },
  cancelled: { text: '已取消', type: 'info' }
}

const statusText = computed(() => statusMap[props.task.status]?.text || '未知')
const statusType = computed(() => statusMap[props.task.status]?.type || 'info')

const progress = computed(() => {
  if (props.task.total_chapters === 0) return 0
  return Math.round((props.task.downloaded_chapters / props.task.total_chapters) * 100)
})

const progressStatus = computed(() => {
  if (props.task.status === 'completed') return 'success'
  if (props.task.status === 'failed') return 'exception'
  return null
})
</script>

<style scoped>
.task-item {
  margin-bottom: 12px;
}

.task-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-info {
  flex: 1;
}

.task-info h4 {
  margin-bottom: 8px;
}

.status {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.progress-text {
  color: #666;
  font-size: 14px;
}

.current {
  color: #409eff;
  font-size: 13px;
  margin-top: 8px;
}

.error {
  color: #f56c6c;
  font-size: 13px;
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.task-actions {
  display: flex;
  gap: 8px;
}
</style>
