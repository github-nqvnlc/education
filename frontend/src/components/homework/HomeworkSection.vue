<script setup>
import { ref, reactive, watchEffect, onMounted } from 'vue'
import { createResource, ListView, ListHeader, ListHeaderItem, ListRow, ListRowItem, Badge, Button } from 'frappe-ui'
import HomeworkSubmission from './HomeworkSubmission.vue'
import { studentStore } from '@/stores/student'
import { formatDateTimeToTimeDMY } from '../../utils/date'

const props = defineProps({
  courseName: {
    type: String,
    required: true
  },
  topicName: {
    type: String,
    required: false,
    default: ''
  }
})

const { studentInfo } = studentStore()

const homeworkList = reactive([])
const homeworkLoading = ref(false)

const tableData = reactive({
  rows: homeworkList,
  columns: [
    { label: 'Title', key: 'title', width: "240px" },
    { label: 'Course', key: 'course', width: "240px" },
    { label: 'Topic', key: 'topic', width: "240px" },
    { label: 'Link', key: 'link_file', width: 1 },
    { label: 'Modified', key: 'modified', width: "200px" },
  ],
})

function loadHomeworks() {
  const studentName = (studentInfo?.name || '').trim()
  if (!studentName) {
    homeworkList.length = 0
    return Promise.resolve()
  }
  homeworkLoading.value = true

  return new Promise((resolve) => {
    createResource({
      url: 'frappe.client.get_list',
      method: 'POST',
      params: {
        doctype: 'Homework',
        fields: ['name', 'title', 'student', 'course', 'topic', 'link_file', 'modified'],
        filters: [['student', '=', studentName], ['topic', '=', props.topicName]],
        order_by: 'modified desc',
        limit_page_length: 20,
      },
      onSuccess: (res) => {
        const data = res?.message || res
        const rows = Array.isArray(data) ? data : (data?.data || [])
        homeworkList.splice(0, homeworkList.length, ...rows)
        homeworkLoading.value = false
        resolve()
      },
      onError: () => {
        homeworkList.length = 0
        homeworkLoading.value = false
        resolve()
      },
    }).submit()
  })
}

// Hàm này sử dụng fetch API để lấy danh sách bài tập về nhà qua endpoint RESTful chuẩn của Frappe
// const homeworkSubmitedList = reactive([])

// async function loadHomeworkList() {
//   const studentName = (studentInfo?.name || '').trim()
//   if (!studentName) {
//     homeworkSubmitedList.length = 0
//     return
//   }
//   homeworkLoading.value = true
//   try {
//     const params = new URLSearchParams({
//       fields: JSON.stringify(['name', 'title', 'student', 'course', 'topic', 'link_file', 'modified']),
//       filters: JSON.stringify([['student', '=', studentName]]),
//       order_by: 'modified desc',
//       limit_page_length: '20'
//     })
//     const url = `/api/resource/Homework?${params.toString()}`
//     const response = await fetch(url, {
//       method: 'GET',
//       headers: {
//         Accept: 'application/json'
//       }
//     })
//     const data = await response.json()
//     const rows = Array.isArray(data?.data) ? data.data : []
//     homeworkSubmitedList.splice(0, homeworkSubmitedList.length, ...rows)
//     console.log('[loadHomeworkList] Homeworks loaded (count=' + homeworkSubmitedList.length + '):')
//     console.table(rows)
//   } catch (err) {
//     homeworkSubmitedList.length = 0
//   } finally {
//     homeworkLoading.value = false
//   }
// }

function onHomeworkSubmitted() {
  console.log('[onHomeworkSubmitted] Homework submitted successfully, reloading list...')
  loadHomeworks()
}

onMounted(async () => {
  await loadHomeworks()
  // await loadHomeworkList()
})
</script>

<template>
  <div class="overflow-hidden rounded-lg shadow-xl bg-white">
    <div class="p-3 md:p-6 border-b border-gray-200 flex items-center justify-between">
      <h4 class="md:text-lg text-base font-semibold">Bài tập về nhà</h4>
      <HomeworkSubmission 
        :student="studentInfo?.name" 
        :course="courseName" 
        :topic="topicName" 
        @submitted="onHomeworkSubmitted"
      />
    </div>
    <div class="p-3 md:p-6">
      <div class="text-sm text-gray-600 mb-2">Danh sách bài đã nộp</div>
      <div v-if="homeworkLoading" class="text-xs text-gray-500">Đang tải...</div>
      <div v-else>
        <div v-if="tableData.rows.length" class="mt-2">
          <ListView :columns="tableData.columns" :rows="tableData.rows" :options="{ selectable: false, showTooltip: false }" row-key="name">
            <ListHeader>
              <ListHeaderItem v-for="column in tableData.columns" :key="column.key" :item="column" />
            </ListHeader>
            <ListRow v-for="row in tableData.rows" :key="row.name" :row="row" v-slot="{ column, item }">
              <ListRowItem :item="item" :align="column.align">
                <template v-if="column.key === 'link_file'">
                  <a
                    v-if="item"
                    :href="item"
                    target="_blank"
                    class="text-blue-600 hover:underline"
                    style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: inline-block; vertical-align: bottom;"
                  >{{ item }}</a>
                  <span v-else class="text-gray-400">—</span>
                </template>
                <template v-else-if="column.key === 'modified'">
                  <p
                    v-if="item"
                    style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: inline-block; vertical-align: bottom;"
                  >{{ formatDateTimeToTimeDMY(item) || '—' }}</p>
                  <p v-else class="text-gray-400">—</p>
                </template>
                <template v-else>
                  <p
                    v-if="item"
                    style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: inline-block; vertical-align: bottom;"
                  >{{ item || '—' }}</p>
                  <p v-else class="text-gray-400">—</p>
                </template>
              </ListRowItem>
            </ListRow>
          </ListView>
        </div>
        <div v-else class="mt-2 p-3 bg-gray-50 border border-gray-200 rounded-md text-xs text-gray-600">
          Chưa có dữ liệu để hiển thị.
        </div>
      </div>
    </div>
  </div>
</template>
