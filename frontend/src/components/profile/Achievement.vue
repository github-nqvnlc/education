<script setup>
import { GRADIENTS } from '@/constants/colors'

defineEmits(['view-progress'])

const achievements = [
  {
    image: 'https://education.windify.edu.vn/files/robot-tham-tu-vang.png',
    title: 'Thám tử săn lỗi',
    description: 'Biết tìm lỗi và sửa lỗi - Sửa 10 lỗi trong bài'
  },
  {
    image: 'https://education.windify.edu.vn/files/phu-thuy-thiet-ke-vang.png',
    title: 'Phù thủy thiết kế',
    description: 'Giao diện & trải nghiệm — Giao diện nhân vật/điều khiển sáng tạo, UI trực quan'
  },
  {
    image: 'https://education.windify.edu.vn/files/ke-chinh-phuc-vang.png',
    title: 'Kẻ chinh phục',
    description: 'Thắng challenge hàng tháng — Giành 1 trong 3 vị trí cuộc thi nội bộ'
  },
  {
    image: 'https://education.windify.edu.vn/files/mat-than-cam-bien-vang.png',
    title: 'Mặt thần cảm biến',
    description: 'Sử dụng cảm biến (ánh sáng, khoảng cách, chạm) - Tạo project phản hồi sensor (ngăn va chạm, dừng khi gần)'
  },
  {
    image: 'https://education.windify.edu.vn/files/dai-su-robot-vang.png',
    title: 'Đại sư robot',
    description: 'Huy hiệu tổng hợp cấp cao — Đạt 5 huy hiệu Gold ở các trụ cột khác nhau'
  },
  {
    image: 'https://education.windify.edu.vn/files/nguoi-dan-chuyen-vang.png',
    title: 'Người dẫn chuyện',
    description: 'Kĩ năng trình bày — Trình bày project trước lớp'
  },
  {
    image: 'https://education.windify.edu.vn/files/anh-hung-cong-dong-vang.png',
    title: 'Anh hùng công đồng',
    description: 'Đóng góp cho cộng đồng — Đóng góp code/tutorial cho lớp, được dùng chung cho lớp'
  }
]
</script>

<template>
  <div class="overflow-hidden rounded-lg shadow-xl">
    <div class="relative text-white p-4" :style="{ background: GRADIENTS.primary }">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold">Huy hiệu</h3>
        <button class="text-sm text-white/90 hover:text-white underline underline-offset-4" @click="$emit('view-progress')">Xem tiến trình</button>
      </div>
    </div>

    <div class="p-4">
      <div class="grid grid-cols-2 sm:grid-cols-7 gap-4">
        <div v-for="(ach, idx) in achievements" :key="idx" class="rounded-lg border-2 border-dashed border-gray-300 p-4 flex flex-col items-center">
          <div>
            <img :src="ach.image" :alt="ach.title">
          </div>
          <div class="mt-2 text-center text-xs text-gray-800 font-medium truncate w-full">{{ ach.title }}</div>
          <div class="mt-1 text-center text-[11px] text-gray-600 line-clamp-2" :title="ach.description">{{ ach.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>




