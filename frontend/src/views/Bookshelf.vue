<template>
  <div class="bookshelf">
    <!-- 添加小说 -->
    <div class="add-section">
      <el-input
        v-model="newUrl"
        placeholder="输入小说目录页URL"
        style="max-width: 500px"
        clearable
      >
        <template #append>
          <el-button type="primary" @click="handleDownload" :loading="downloading">
            下载
          </el-button>
        </template>
      </el-input>
      <el-input
        v-model="newTags"
        placeholder="标签（可选，逗号分隔）"
        style="max-width: 200px; margin-left: 10px"
        clearable
      />
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <el-input
        v-model="keyword"
        placeholder="搜索书名或作者"
        style="max-width: 300px"
        clearable
        @keyup.enter="loadNovels"
      >
        <template #append>
          <el-button @click="loadNovels">搜索</el-button>
        </template>
      </el-input>
    </div>

    <!-- 小说列表 -->
    <div class="novel-grid" v-loading="loading">
      <NovelCard
        v-for="novel in novels"
        :key="novel.id"
        :novel="novel"
        @click="goToDetail(novel.id)"
      />
    </div>

    <!-- 空状态 -->
    <el-empty v-if="!loading && novels.length === 0" description="书架空空如也" />

    <!-- 分页 -->
    <div class="pagination" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="loadNovels"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { novelApi, downloadApi } from '../api'
import NovelCard from '../components/NovelCard.vue'

const router = useRouter()

const novels = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const keyword = ref('')

const newUrl = ref('')
const newTags = ref('')
const downloading = ref(false)

const loadNovels = async () => {
  loading.value = true
  try {
    const data = await novelApi.getList({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value || undefined
    })
    novels.value = data.items
    total.value = data.total
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    loading.value = false
  }
}

const handleDownload = async () => {
  if (!newUrl.value) {
    ElMessage.warning('请输入小说URL')
    return
  }

  downloading.value = true
  try {
    await downloadApi.start({
      url: newUrl.value,
      tags: newTags.value || undefined
    })
    ElMessage.success('已开始下载')
    newUrl.value = ''
    newTags.value = ''
    router.push('/download')
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    downloading.value = false
  }
}

const goToDetail = (id) => {
  router.push(`/novel/${id}`)
}

onMounted(() => {
  loadNovels()
})
</script>

<style scoped>
.bookshelf {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.add-section {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.filter-section {
  margin-bottom: 20px;
}

.novel-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
