<template>
  <el-card class="novel-card" shadow="hover" @click="$emit('click')">
    <div class="card-content">
      <div class="cover">
        <el-image
          v-if="novel.cover_url"
          :src="novel.cover_url"
          fit="cover"
        >
          <template #error>
            <div class="cover-placeholder">
              <el-icon><Document /></el-icon>
            </div>
          </template>
        </el-image>
        <div v-else class="cover-placeholder">
          <el-icon><Document /></el-icon>
        </div>
      </div>
      <div class="info">
        <h3 class="title">{{ novel.title }}</h3>
        <p class="author" v-if="novel.author">{{ novel.author }}</p>
        <p class="chapters">{{ novel.total_chapters }} 章</p>
        <el-tag v-if="novel.status" size="small" :type="novel.status === '已完结' ? 'success' : ''">
          {{ novel.status }}
        </el-tag>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { Document } from '@element-plus/icons-vue'

defineProps({
  novel: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])
</script>

<style scoped>
.novel-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.novel-card:hover {
  transform: translateY(-4px);
}

.card-content {
  display: flex;
  gap: 12px;
}

.cover {
  width: 80px;
  height: 110px;
  flex-shrink: 0;
}

.cover .el-image,
.cover-placeholder {
  width: 100%;
  height: 100%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.cover-placeholder .el-icon {
  font-size: 32px;
  color: #ccc;
}

.info {
  flex: 1;
  min-width: 0;
}

.title {
  font-size: 16px;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.author,
.chapters {
  font-size: 13px;
  color: #666;
  margin-bottom: 4px;
}
</style>
