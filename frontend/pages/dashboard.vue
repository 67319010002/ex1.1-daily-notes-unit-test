<template>
  <div class="p-6 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">My Notes</h1>

    <!-- Tabs -->
    <div class="flex gap-4 mb-4">
      <button
        :class="activeTab === 'all' ? 'font-bold underline' : ''"
        @click="switchTab('all')"
      >
        All Notes
      </button>
      <button
        :class="activeTab === 'search' ? 'font-bold underline' : ''"
        @click="switchTab('search')"
      >
        Search
      </button>
    </div>

    <!-- Create Note -->
    <div v-if="activeTab === 'all'" class="flex gap-2 mb-4">
      <input v-model="title" placeholder="Title" class="border p-2 w-1/3" />
      <input v-model="content" placeholder="Content" class="border p-2 flex-1" />
      <button @click="createNote" class="bg-green-500 text-white p-2">Add</button>
    </div>

    <!-- Search Notes -->
    <div v-if="activeTab === 'search'" class="flex gap-2 mb-4">
      <input v-model="searchQuery" placeholder="Search notes..." class="border p-2 flex-1" />
      <button @click="searchNotes" class="bg-blue-500 text-white p-2">Search</button>
    </div>

    <!-- Notes List -->
    <NoteCard
      v-for="note in notes"
      :key="note.id"
      :note="note"
      @delete="deleteNote"
    />
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const title = ref('')
const content = ref('')
const searchQuery = ref('')
const notes = ref([])
const activeTab = ref('all')

const token = localStorage.getItem('token')

const fetchNotes = async () => {
  const res = await axios.get('http://localhost:5000/api/notes', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  notes.value = res.data
}

const createNote = async () => {
  try {
    await axios.post('http://localhost:5000/api/notes', {
      title: title.value,
      content: content.value
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    title.value = ''
    content.value = ''
    fetchNotes()
  } catch (e) {
    console.error('Create note failed:', e)
  }
}

const deleteNote = async (id) => {
  await axios.delete(`http://localhost:5000/api/notes/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  fetchNotes()
}

const searchNotes = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/api/notes/search?q=${encodeURIComponent(searchQuery.value)}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    notes.value = res.data
  } catch (e) {
    console.error('Search failed:', e)
  }
}

const switchTab = (tab) => {
  activeTab.value = tab
  if (tab === 'all') fetchNotes()
  if (tab === 'search') notes.value = [] // clear previous results
}

onMounted(fetchNotes)
</script>
