<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const email = ref('')
const newPassword = ref('')
const loading = ref(false)

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const changePassword = async () => {
  if (!email.value || !newPassword.value) {
    toast.error('Both email and new password are required.')
    return
  }

  loading.value = true
  try {
    await axios.post('https://bidngive.onrender.com/api/admin/user/change-password/', {
      email: email.value,
      new_password: newPassword.value,
    }, { headers })

    toast.success(`Password changed successfully for ${email.value}`)
    email.value = ''
    newPassword.value = ''
  } catch (err) {
    toast.error(err.response?.data?.error || 'Failed to change password.')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="password-container">
    <h2>🔐 Admin: Change User Password</h2>

    <div class="form-group">
      <label>Email</label>
      <input
        type="email"
        v-model="email"
        placeholder="Enter user email"
        class="input"
      />
    </div>

    <div class="form-group">
      <label>New Password</label>
      <input
        type="password"
        v-model="newPassword"
        placeholder="Enter new password"
        class="input"
      />
    </div>

    <button @click="changePassword" :disabled="loading" class="action-btn">
      {{ loading ? 'Updating...' : 'Change Password' }}
    </button>
  </main>
</template>

<style scoped>
.password-container {
  max-width: 500px;
  margin: 50px auto;
  padding: 30px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  font-family: 'Inter', sans-serif;
}

h2 {
  font-size: 1.5em;
  margin-bottom: 1.5em;
  text-align: center;
  color: #222;
}

.form-group {
  margin-bottom: 1.2em;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
  color: #333;
}

.input {
  width: 100%;
  padding: 10px 12px;
  font-size: 0.95em;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #f9f9f9;
  outline: none;
}

.input:focus {
  border-color: #17a35e;
  background: #fff;
}

.action-btn {
  width: 100%;
  background-color: #17a35e;
  color: white;
  padding: 12px;
  font-weight: 600;
  font-size: 1em;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s ease-in-out;
}

.action-btn:hover {
  background-color: #139c57;
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
