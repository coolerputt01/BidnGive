<template>
  <main class="merge-settings">
    <h2>⚙️ Auction Merge Settings</h2>
    <p>Adjust merge times and auction duration below.</p>

    <form @submit.prevent="updateSettings" class="settings-form">
      <div class="form-group">
        <label>🕗 Morning Time</label>
        <input type="time" v-model="form.morning_time" required />
      </div>
      <div class="form-group">
        <label>🌙 Evening Time</label>
        <input type="time" v-model="form.evening_time" required />
      </div>
      <div class="form-group">
        <label>⏱ Auction Duration (minutes)</label>
        <input type="number" v-model="form.auction_duration_minutes" min="1" required />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Saving...' : 'Save Changes' }}
      </button>
    </form>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const form = ref({
  morning_time: '',
  evening_time: '',
  auction_duration_minutes: 3
})

const loading = ref(false)

const fetchSettings = async () => {
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/admin/merge/settings/', { headers })
    form.value = { ...form.value, ...res.data }
  } catch {
    toast.error('Failed to load settings.')
  }
}

const updateSettings = async () => {
  loading.value = true
  try {
    await axios.patch('https://bidngive.onrender.com/api/admin/merge/settings/', form.value, { headers })
    toast.success('Settings updated successfully.')
  } catch {
    toast.error('Failed to update settings.')
  } finally {
    loading.value = false
  }
}

onMounted(fetchSettings)
</script>

<style scoped>
.merge-settings {
  max-width: 600px;
  margin: 3rem auto;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  font-family: 'Segoe UI', sans-serif;
}

h2 {
  margin-bottom: 1rem;
  color: #0a6847;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.3rem;
  font-weight: 600;
}

input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

button {
  padding: 12px;
  background: #0a6847;
  color: white;
  border: none;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
}

button:disabled {
  background: #8bc6a4;
  cursor: not-allowed;
}
</style>
