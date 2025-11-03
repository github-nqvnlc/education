<script setup>
import { ref, reactive, watch } from 'vue'
import { Dialog, FormControl, Textarea, Button as FButton, createResource } from 'frappe-ui'
import { toastError, toastSuccess } from '@/utils'

const props = defineProps({
  student: { type: String, default: '' },
  course: { type: String, default: '' },
  topic: { type: String, default: '' },
})

const emit = defineEmits(['submitted'])

const show = ref(false)
const isSubmitting = ref(false)
const selectedFile = ref(null)
const form = reactive({
  title: '',
  student: '',
  course: '',
  topic: '',
  link_file_homework: '',
  description: '',
})

const validationErrors = reactive({
  student: '',
  course: '',
  topic: '',
  link_file_homework: '',
})

function open(student, course, topicName) {
  form.student = student || props.student || ''
  form.course = course || props.course || ''
  form.topic = topicName || props.topic || ''
  form.title = ''
  form.link_file_homework = ''
  form.description = ''
  validationErrors.student = ''
  validationErrors.course = ''
  validationErrors.topic = ''
  validationErrors.link_file_homework = ''
  selectedFile.value = null
  show.value = true
}

defineExpose({ open })

function validateForm() {
  let isValid = true
  validationErrors.student = ''
  validationErrors.course = ''
  validationErrors.topic = ''
  validationErrors.link_file_homework = ''

  const studentName = form.student
  const courseValue = form.course
  const topicValue = form.topic
  const linkFile = form.link_file_homework

  if (!studentName) {
    validationErrors.student = 'Học sinh là bắt buộc'
    isValid = false
  }
  if (!courseValue) {
    validationErrors.course = 'Bài học là bắt buộc'
    isValid = false
  }
  if (!topicValue) {
    validationErrors.topic = 'Chủ đề là bắt buộc'
    isValid = false
  }
  if (!linkFile) {
    validationErrors.link_file_homework = 'Link file bài tập là bắt buộc'
    isValid = false
  }
  return isValid
}

function handleFileChange(e) {
  const files = e?.target?.files || []
  selectedFile.value = files[0] || null
}

function handleSubmit(close) {
  if (!validateForm()) {
    toastError({
      title: 'Thiếu trường bắt buộc',
      message: 'Vui lòng điền đầy đủ các trường bắt buộc'
    })
    return
  }

  const payload = {
    title: form.title,
    student: form.student,
    course: form.course,
    topic: form.topic,
    link_file: form.link_file_homework,
    description: form.description,
  }

  const createHomework = createResource({
    url: `/api/resource/Homework`,
    method: 'POST',
    onSuccess() {
      isSubmitting.value = false
      toastSuccess({ title: 'Bài tập đã được nộp thành công', message: 'Bài tập đã được nộp!' })
      emit('submitted')
      close?.()
    },
    onError(err) {
      isSubmitting.value = false
      toastError({ title: 'Lỗi khi nộp bài tập', message: err?.message || 'Lỗi khi nộp bài tập' })
    },
  })

  isSubmitting.value = true
  createHomework.submit(payload)
}
// keep form in sync if props change while dialog is open
watch(
  () => [props.student, props.course],
  ([s, c]) => {
    if (show.value) {
      form.student = s || form.student
      form.course = c || form.course
    }
  }
)

</script>

<template>
  <div>
    <FButton variant="solid" @click="open(props.student, props.course, props.topic)">Nộp bài</FButton>
    <Dialog v-model="show" :options="{ title: 'Nộp bài tập', size: 'xl' }">
      <template #body-content>
        <div class="grid md:grid-cols-2 grid-cols-1 gap-6">
          <!-- Left column -->
          <div class="space-y-4">
            <div>
              <div class="mb-2 text-sm text-gray-600">Tiêu đề</div>
              <FormControl type="text" v-model="form.title" placeholder="Nhập tiêu đề" />
            </div>
            <div>
              <div class="mb-2 text-sm text-gray-600">Học sinh <span class="text-red-500">*</span></div>
              <FormControl type="text" v-model="form.student" :disabled="true" :placeholder="form.student" :class="{ 'border-red-500': validationErrors.student }" />
              <div v-if="validationErrors.student" class="mt-1 text-xs text-red-600">{{ validationErrors.student }}</div>
            </div>
            <div>
              <div class="mb-2 text-sm text-gray-600">Khóa học <span class="text-red-500">*</span></div>
              <FormControl type="text" v-model="form.course" :disabled="true" :placeholder="form.course" :class="{ 'border-red-500': validationErrors.course }" />
              <div v-if="validationErrors.course" class="mt-1 text-xs text-red-600">{{ validationErrors.course }}</div>
            </div>
            <div>
              <div class="mb-2 text-sm text-gray-600">Bài học <span class="text-red-500">*</span></div>
              <FormControl type="text" v-model="form.topic" :disabled="true" :placeholder="form.topic" :class="{ 'border-red-500': validationErrors.topic }" />
              <div v-if="validationErrors.topic" class="mt-1 text-xs text-red-600">{{ validationErrors.topic }}</div>
            </div>
          </div>

          <!-- Right column -->
          <div class="space-y-4">
            <div>
              <div class="mb-2 text-sm text-gray-600">Link File bài tập <span class="text-red-500">*</span></div>
              <FormControl type="text" v-model="form.link_file_homework" placeholder="https://..." :class="{ 'border-red-500': validationErrors.link_file_homework }" />
              <div v-if="validationErrors.link_file_homework" class="mt-1 text-xs text-red-600">{{ validationErrors.link_file_homework }}</div>
            </div>
            <div>
              <div class="mb-2 text-sm text-gray-600">File bài tập</div>
              <div class="flex items-center gap-3">
                <label class="inline-flex items-center px-3 py-1.5 rounded-md border cursor-pointer text-sm hover:bg-gray-50"
                  :style="{ borderColor: 'var(--color-primary)', color: 'var(--color-primary)' }">
                  <input type="file" class="hidden" @change="handleFileChange" />
                  Attach
                </label>
                <div class="text-xs text-gray-500 truncate max-w-[200px]" v-if="selectedFile?.name">{{ selectedFile.name }}</div>
              </div>
            </div>
            <div>
              <div class="mb-2 text-sm text-gray-600">Mô tả</div>
              <Textarea rows="8" v-model="form.description" placeholder="Mô tả ngắn..." />
            </div>
          </div>
        </div>
      </template>
      <template #actions="{ close }">
        <div class="flex flex-row-reverse gap-2">
          <FButton variant="solid" :loading="isSubmitting" :disabled="isSubmitting" @click="handleSubmit(close)">Nộp bài</FButton>
          <FButton variant="subtle" @click="close" :disabled="isSubmitting">Hủy</FButton>
        </div>
      </template>
    </Dialog>
  </div>
  
</template>

<style scoped>
</style>


