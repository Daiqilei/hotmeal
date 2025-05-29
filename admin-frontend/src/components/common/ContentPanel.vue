<template>
  <div class="content-panel">
    <!-- 搜索区域插槽 -->
    <div class="upper">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <slot :form="searchForm" :onReset="resetSearch" :onSearch="handleSearch" name="search-form">
          <!-- 默认搜索插槽（如果未提供） -->
          <el-form-item label="关键词">
            <el-input v-model="searchForm.keyword" clearable placeholder="请输入关键词" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </slot>
      </el-form>

      <!-- 按钮插槽 -->
      <div class="button-group">
        <slot :selected="multipleSelection" name="toolbar" />
      </div>
    </div>

    <!-- 表格 -->
    <el-table :data="dataList" style="width: 100%" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" />
      <slot name="columns">
        <!-- 默认列 -->
        <el-table-column label="ID" prop="id" />
        <el-table-column label="名称" prop="name" />
      </slot>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      v-model:current-page="page"
      :page-size="pageSize"
      :total="total"
      class="pagination"
      layout="prev, pager, next"
      @current-change="handleSearch"
    />

    <!-- 默认插槽：允许 Profile.vue 中插入的自定义内容渲染 -->
    <slot />
  </div>
</template>

<script setup>
  import { onMounted, ref } from 'vue'

  const props = defineProps({
    fetchData: Function, // (query) => Promise<{ list:[], total: number }>
    initQuery: Object
  })

  const emits = defineEmits(['update:selected'])

  const searchForm = ref({ ...(props.initQuery || {}) })
  const dataList = ref([])
  const multipleSelection = ref([])
  const page = ref(1)
  const pageSize = 10
  const total = ref(0)

  const handleSearch = async () => {
    //console.log('[ContentPanel] handleSearch start')
    //console.log('[ContentPanel] before query, searchForm:', searchForm.value, 'page:', page.value)
    const query = { ...searchForm.value, page: page.value, pageSize }
    //console.log('[ContentPanel] handleSearch query:', query)
    const res = await props.fetchData?.(query)
    //console.log('[ContentPanel] handleSearch res:', res)
    /* console.log(
     '[ContentPanel] dataArr before set:',
     res?.list || res?.data || [],
     'total before set:',
     res?.total,
   )*/
    dataList.value = (res?.list || []).slice().sort((a, b) => {
      const getKey = (item) => ('_sortKey' in item ? item._sortKey : item[Object.keys(item || {})[0]])
      return (getKey(a) ?? 0) - (getKey(b) ?? 0)
    })
    total.value = res?.total || 0
    //console.log('[ContentPanel] after set, dataList:', dataList.value, 'total:', total.value)
  }

  const resetSearch = () => {
    Object.keys(searchForm.value).forEach((key) => (searchForm.value[key] = ''))
    page.value = 1
    handleSearch()
  }

  const handleSelectionChange = (val) => {
    multipleSelection.value = val
    emits('update:selected', val)
  }

  onMounted(handleSearch)
  defineExpose({
    fetchData: handleSearch
  })
</script>

<style scoped>
  .upper {
    display: flex;
    justify-content: space-between;
  }

  .content-panel {
    padding: 20px;
  }

  .search-form {
    margin-bottom: 20px;
  }

  .button-group {
    margin-bottom: 10px;
  }

  .pagination {
    margin-top: 15px;
    text-align: right;
  }
</style>
