<template>
  <Dropdown v-model:show="userMenuOpen" :options="userDropdownOptions"
    class="p-2 flex items-center justify-center w-full">
    <template v-slot="{ open }">
      <button
        class="group flex h-12 items-center rounded-md border border-gray-200/60 bg-white/70 px-1 shadow-sm backdrop-blur transition duration-200 ease-in-out"
        :class="isCollapsed
            ? 'w-auto'
            : open
              ? 'ring-1 ring-[#FF6B35] w-[232px]'
              : 'hover:bg-white hover:shadow hover:ring-1 hover:ring-[#FF6B35] w-[232px]'
          " aria-label="User menu">
        <div class="w-9 h-9 rounded-full flex items-center justify-center overflow-hidden bg-gray-100">
          <Avatar v-if="educationSettings?.logo" :image="educationSettings?.logo" shape="circle" size="xl" />
          <Avatar v-else-if="user?.data?.user_image" :image="user.data.user_image" :label="user?.data?.full_name"
            shape="circle" size="xl" />
          <Avatar v-else :label="user?.data?.full_name || 'U'" shape="circle" size="xl" />
        </div>
        <div class="flex flex-1 min-w-0 flex-col text-left transition duration-200 ease-in-out" :class="isCollapsed
            ? 'opacity-0 ml-0 w-0 overflow-hidden'
            : 'opacity-100 ml-3 w-auto'
          ">
          <div class="truncate text-sm font-medium text-gray-900 leading-tight">
            {{ educationSettings?.name || 'Education' }}
          </div>
          <div class="mt-0.5 truncate text-xs text-gray-600 leading-tight">
            <span v-if="user?.loading" class="inline-block h-3 w-24 animate-pulse rounded bg-gray-200"></span>
            <span v-else>{{ user?.data?.full_name }}</span>
          </div>
        </div>

        <div class="transition-transform duration-200 ease-in-out" :class="isCollapsed
            ? 'opacity-0 ml-0 w-0 overflow-hidden'
            : open
              ? 'rotate-180 ml-2'
              : 'ml-2'
          ">
          <FeatherIcon name="chevron-down" class="h-4 w-4 text-gray-600 group-hover:text-gray-800" aria-hidden="true" />
        </div>
      </button>
    </template>
  </Dropdown>

  <ProfileModal />
</template>

<script setup>
import { Dropdown, FeatherIcon, Avatar } from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import { usersStore } from '@/stores/user'
import { provide, ref } from 'vue'
import ProfileModal from '@/components/profile/ProfileModal.vue'
import { useRouter } from 'vue-router'

const { user } = usersStore()
const { logout } = sessionStore()
const router = useRouter()
defineOptions({
  inheritAttrs: false,
})

const props = defineProps({
  isCollapsed: {
    type: Boolean,
    default: false,
  },
  educationSettings: {},
})

const showProfileDialog = ref(false)
const userMenuOpen = ref(false)
provide('showProfileDialog', showProfileDialog)

const userDropdownOptions = [
  // Only show Test Doctype API menu for specific email
  ...(user.data?.email === 'thinhtn.itedu@gmail.com' ? [{
    icon: 'book-open-check',
    label: 'Test Doctype API',
    onClick: () => {
      console.log('user.data', user.data)
      router.push('/doctype-tester')
    },
  }] : []),
  {
    icon: 'log-out',
    label: 'Đăng xuất',
    onClick: () => logout.submit(),
  }
]
</script>
