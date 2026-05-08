<template>
  <div class="rule-config">
    <div class="header">
      <h2>规则配置</h2>
      <el-button type="primary" @click="showDialog()">新增规则</el-button>
    </div>

    <el-table :data="rules" v-loading="loading">
      <el-table-column prop="site_name" label="网站名称" />
      <el-table-column prop="site_url" label="网站地址" />
      <el-table-column prop="rule_type" label="类型">
        <template #default="{ row }">
          <el-tag :type="row.rule_type === 'specific' ? 'primary' : 'info'">
            {{ row.rule_type === 'specific' ? '特定适配' : '通用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="状态">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'">
            {{ row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="testRule(row)">测试</el-button>
          <el-button size="small" @click="showDialog(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="editingRule ? '编辑规则' : '新增规则'" width="600px">
      <el-form :model="form" label-width="120px">
        <el-form-item label="网站名称" required>
          <el-input v-model="form.site_name" />
        </el-form-item>
        <el-form-item label="网站地址" required>
          <el-input v-model="form.site_url" />
        </el-form-item>
        <el-form-item label="规则类型">
          <el-radio-group v-model="form.rule_type">
            <el-radio value="generic">通用</el-radio>
            <el-radio value="specific">特定适配</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="书名选择器">
          <el-input v-model="form.selectors.book_title" placeholder="如: h1.title" />
        </el-form-item>
        <el-form-item label="作者选择器">
          <el-input v-model="form.selectors.book_author" placeholder="如: .author" />
        </el-form-item>
        <el-form-item label="章节列表选择器">
          <el-input v-model="form.selectors.chapter_list" placeholder="如: #list a" />
        </el-form-item>
        <el-form-item label="内容选择器">
          <el-input v-model="form.selectors.chapter_content" placeholder="如: #content" />
        </el-form-item>
        <el-form-item label="需要JS渲染">
          <el-switch v-model="form.requires_js" />
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>

    <!-- 测试结果弹窗 -->
    <el-dialog v-model="testDialogVisible" title="测试结果" width="500px">
      <pre class="test-result">{{ testResult }}</pre>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ruleApi } from '../api'

const rules = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const testDialogVisible = ref(false)
const testResult = ref('')
const editingRule = ref(null)

const form = reactive({
  site_name: '',
  site_url: '',
  rule_type: 'generic',
  is_active: true,
  requires_js: false,
  selectors: {
    book_title: '',
    book_author: '',
    chapter_list: '',
    chapter_content: ''
  }
})

const loadRules = async () => {
  loading.value = true
  try {
    const data = await ruleApi.getList()
    rules.value = data.items
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    loading.value = false
  }
}

const showDialog = (rule = null) => {
  editingRule.value = rule
  if (rule) {
    Object.assign(form, {
      site_name: rule.site_name,
      site_url: rule.site_url,
      rule_type: rule.rule_type,
      is_active: rule.is_active,
      requires_js: rule.requires_js,
      selectors: rule.selectors || {}
    })
  } else {
    Object.assign(form, {
      site_name: '',
      site_url: '',
      rule_type: 'generic',
      is_active: true,
      requires_js: false,
      selectors: {
        book_title: '',
        book_author: '',
        chapter_list: '',
        chapter_content: ''
      }
    })
  }
  dialogVisible.value = true
}

const handleSave = async () => {
  try {
    if (editingRule.value) {
      await ruleApi.update(editingRule.value.id, form)
      ElMessage.success('更新成功')
    } else {
      await ruleApi.create(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    await loadRules()
  } catch (error) {
    ElMessage.error(error.message)
  }
}

const handleDelete = async (ruleId) => {
  try {
    await ElMessageBox.confirm('确定要删除这个规则吗？', '提示', { type: 'warning' })
    await ruleApi.delete(ruleId)
    ElMessage.success('删除成功')
    await loadRules()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message)
    }
  }
}

const testRule = async (rule) => {
  const testUrl = await ElMessageBox.prompt('请输入测试URL', '测试规则', {
    inputPattern: /^https?:\/\/.+/,
    inputErrorMessage: '请输入有效的URL'
  }).catch(() => null)

  if (!testUrl) return

  try {
    ElMessage.info('正在测试...')
    const result = await ruleApi.test({
      rule_id: rule.id,
      test_url: testUrl.value
    })

    testResult.value = JSON.stringify(result, null, 2)
    testDialogVisible.value = true

    if (result.success) {
      ElMessage.success('测试成功')
    } else {
      ElMessage.error(result.message)
    }
  } catch (error) {
    ElMessage.error(error.message)
  }
}

onMounted(() => {
  loadRules()
})
</script>

<style scoped>
.rule-config {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.test-result {
  background-color: #f5f5f5;
  padding: 16px;
  border-radius: 4px;
  overflow: auto;
  max-height: 400px;
}
</style>
