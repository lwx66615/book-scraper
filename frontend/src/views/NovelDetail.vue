<template>
  <div class="novel-detail" v-loading="loading">
    <template v-if="novel">
      <!-- 基本信息 -->
      <el-card class="info-card">
        <div class="novel-header">
          <div class="cover">
            <el-image v-if="novel.cover_url" :src="novel.cover_url" fit="cover">
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
            <h1>{{ novel.title }}</h1>
            <p class="author" v-if="novel.author">作者：{{ novel.author }}</p>
            <p class="source">来源：{{ novel.source_site }}</p>
            <el-tag :type="novel.status === '已完结' ? 'success' : ''">
              {{ novel.status }}
            </el-tag>
            <p class="description" v-if="novel.description">{{ novel.description }}</p>
          </div>
          <div class="actions">
            <el-button type="primary" @click="handleExport('txt')">导出TXT</el-button>
            <el-button type="primary" @click="handleExport('epub')">导出EPUB</el-button>
            <el-button @click="checkUpdate">检查更新</el-button>
            <el-button type="danger" @click="handleDelete">删除</el-button>
          </div>
        </div>
      </el-card>

      <!-- 章节列表 -->
      <el-card class="chapters-card">
        <template #header>
          <div class="chapters-header">
            <span>章节列表 ({{ novel.total_chapters }}章)</span>
            <el-input
              v-model="chapterKeyword"
              placeholder="搜索章节"
              style="width: 200px"
              clearable
            />
          </div>
        </template>

        <div class="chapters-grid">
          <div
            v-for="chapter in filteredChapters"
            :key="chapter.id"
            class="chapter-item"
            @click="showChapter(chapter)"
          >
            {{ chapter.title }}
          </div>
        </div>

        <el-empty v-if="chapters.length === 0" description="暂无章节" />
      </el-card>
    </template>

    <!-- 章节内容弹窗 -->
    <el-dialog v-model="chapterDialogVisible" :title="currentChapter?.title" width="60%">
      <div class="chapter-content" v-loading="chapterLoading">
        {{ currentChapterContent }}
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document } from '@element-plus/icons-vue'
import { novelApi, exportApi } from '../api'

const route = useRoute()
const router = useRouter()

const novel = ref(null)
const chapters = ref([])
const loading = ref(false)
const chapterKeyword = ref('')

const chapterDialogVisible = ref(false)
const currentChapter = ref(null)
const currentChapterContent = ref('')
const chapterLoading = ref(false)

const filteredChapters = computed(() => {
  if (!chapterKeyword.value) return chapters.value
  return chapters.value.filter(c =>
    c.title.toLowerCase().includes(chapterKeyword.value.toLowerCase())
  )
})

const loadNovel = async () => {
  loading.value = true
  try {
    novel.value = await novelApi.getDetail(route.params.id)
    const data = await novelApi.getChapters(route.params.id, { page_size: 1000 })
    chapters.value = data.items
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    loading.value = false
  }
}

const showChapter = async (chapter) => {
  currentChapter.value = chapter
  chapterDialogVisible.value = true
  chapterLoading.value = true

  try {
    const data = await novelApi.getChapter(chapter.id)
    currentChapterContent.value = data.content || '内容为空'
  } catch (error) {
    ElMessage.error(error.message)
    currentChapterContent.value = '加载失败'
  } finally {
    chapterLoading.value = false
  }
}

const handleExport = async (type) => {
  try {
    const response = type === 'txt'
      ? await exportApi.txt(novel.value.id)
      : await exportApi.epub(novel.value.id)

    // 创建下载链接
    const blob = new Blob([response], {
      type: type === 'txt' ? 'text/plain' : 'application/epub+zip'
    })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${novel.value.title}.${type}`
    a.click()
    window.URL.revokeObjectURL(url)

    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error(error.message)
  }
}

const checkUpdate = async () => {
  ElMessage.info('检查更新功能开发中')
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这本小说吗？', '提示', {
      type: 'warning'
    })

    await novelApi.delete(novel.value.id)
    ElMessage.success('删除成功')
    router.push('/')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message)
    }
  }
}

onMounted(() => {
  loadNovel()
})
</script>

<style scoped>
.novel-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.info-card {
  margin-bottom: 20px;
}

.novel-header {
  display: flex;
  gap: 24px;
}

.cover {
  width: 150px;
  height: 200px;
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
  font-size: 48px;
  color: #ccc;
}

.info {
  flex: 1;
}

.info h1 {
  margin-bottom: 12px;
}

.author,
.source {
  color: #666;
  margin-bottom: 8px;
}

.description {
  margin-top: 12px;
  color: #333;
  line-height: 1.6;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chapters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chapters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 8px;
  max-height: 500px;
  overflow-y: auto;
}

.chapter-item {
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chapter-item:hover {
  background-color: #f0f0f0;
}

.chapter-content {
  white-space: pre-wrap;
  line-height: 1.8;
  max-height: 60vh;
  overflow-y: auto;
}
</style>
