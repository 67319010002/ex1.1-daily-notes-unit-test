<template>
  <nav class="bg-black text-white px-6 py-4 flex items-center shadow-md">
    <NuxtLink to="dashboard" class="font-bold text-2xl hover:text-gray-300 transition flex-shrink-0">
      DailyNotes
    </NuxtLink>

    <div class="ml-auto relative">
      <button
        @click="toggleDropdown"
        class="p-2 rounded hover:bg-gray-800 transition"
        aria-label="Settings"
      >
        ⚙️
      </button>

      <div
        v-if="dropdownOpen"
        class="absolute right-0 mt-2 w-40 bg-gray-900 rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-50"
      >
        <NuxtLink
          to="/login"
          class="block px-4 py-2 text-white hover:bg-gray-700 transition transform hover:scale-110 hover:-translate-y-1"
          @click="closeDropdown"
        >
          Login
        </NuxtLink>
        <NuxtLink
          to="/register"
          class="block px-4 py-2 text-white hover:bg-gray-700 transition transform hover:scale-110 hover:-translate-y-1"
          @click="closeDropdown"
        >
          Register
        </NuxtLink>
        <NuxtLink
          to="/dashboard"
          class="block px-4 py-2 text-white hover:bg-gray-700 transition transform hover:scale-110 hover:-translate-y-1"
          @click="closeDropdown"
        >
          Dashboard
        </NuxtLink>
        <button
          @click="handleLogout"
          class="w-full text-left px-4 py-2 text-red-400 hover:bg-gray-700 transition transform hover:scale-110 hover:-translate-y-1"
        >
          Logout
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const dropdownOpen = ref(false)

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const handleLogout = () => {
  localStorage.removeItem('token')
  dropdownOpen.value = false
  router.push('/login')
}
</script>
