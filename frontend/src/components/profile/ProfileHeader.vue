<template>
  <div
    class="col-span-1 overflow-hidden rounded-lg shadow-xlrelative text-white p-4 flex flex-col md:flex-row gap-4"
    style="background: linear-gradient(90deg, rgb(242, 90, 35) 0%, rgb(241, 146, 85) 100%);"
  >
    <div class="sm:size-60 md:size-56 size-40 aspect-square rounded-lg overflow-hidden bg-gray-200">
      <img
        v-if="studentInfo?.image?.length > 0"
        :src="studentInfo?.image"
        class="sm:size-60 md:size-56 size-40 aspect-square object-cover bg-transparent"
      />
      <div
        v-else
        class="sm:size-60 md:size-56 size-40 aspect-square grid place-items-center text-[24px] font-semibold text-slate-500"
      >
        {{ firstInitial }}
      </div>
    </div>
    <div class="min-w-0">
      <div class="md:text-[40px] sm:text-[32px] text-[28px] font-extrabold truncate">
        {{ studentInfo?.student_name }}
      </div>
      <div class="flex flex-col gap-1">
        <span class="py-1 text-white/90 text-sm">{{ user?.data?.email }}</span>
        <p
          class="px-4 py-1 text-xl font-semibold rounded bg-white/20 w-fit"
          style="background: linear-gradient(90deg, #224773 0%, #4086D9 100%);"
        >
          Học viên
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  studentInfo: { type: Object, default: () => ({}) },
  user: { type: Object, default: () => ({}) },
})

const firstInitial = computed(() => {
  const name = props.studentInfo?.student_name || props.user?.data?.student_name || ''
  return name.trim().charAt(0).toUpperCase()
})
</script>

<style scoped>
</style>


