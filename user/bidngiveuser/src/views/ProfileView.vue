<template>
  <main class="profile-page">
    <section class="profile-header">
      <img src="/icons/profile.svg" alt="Profile" class="profile-avatar" />
      <h2>{{ user.full_name }}</h2>
      <p>{{ user.email }}</p>
    </section>

    <section class="profile-details" v-if="!loading">
      <div class="detail-item">
        <label>Full Name</label>
        <input type="text" v-model="user.username" disabled />
      </div>

      <div class="detail-item">
        <label>Email</label>
        <input type="email" v-model="user.email" disabled />
      </div>

      <div class="detail-item">
        <label>Phone Number</label>
        <input type="tel" v-model="user.phone" disabled />
      </div>

      <div class="detail-item">
        <label>Referral Code</label>
        <div class="referral-box">
          <input type="text" :value="user.referral_code" readonly />
          <button @click="copyReferral">Copy</button>
        </div>
      </div>
    </section>

    <div v-if="copied" class="copied-banner">Copied to clipboard ✅</div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const user = ref({})
const copied = ref(false)
const loading = ref(true)
const token = localStorage.getItem('access_token')

const fetchProfile = async () => {
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/accounts/me/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = res.data
  } catch (err) {
    toast.error('Failed to load profile')
  } finally {
    loading.value = false
  }
}

const copyReferral = () => {
  navigator.clipboard.writeText(user.value.referral_code)
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}

onMounted(fetchProfile)
</script>

<style scoped>
.profile-page {
  padding: 20px;
  background-color: #f5f5f5;
  font-family: Arial, sans-serif;
  min-height: 100vh;
}

.profile-header {
  text-align: center;
  margin-bottom: 25px;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 10px;
  background-color: #ddd;
}

.profile-header h2 {
  font-size: 1.6em;
  margin: 5px 0;
}

.profile-header p {
  font-size: 0.95em;
  color: #666;
}

.profile-details {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  max-width: 500px;
  margin: auto;
}

.detail-item {
  margin-bottom: 15px;
}

.detail-item label {
  font-weight: 600;
  display: block;
  margin-bottom: 6px;
  color: #333;
}

.detail-item input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1em;
}

.referral-box {
  display: flex;
  gap: 10px;
}

.referral-box input {
  flex: 1;
}

.referral-box button {
  padding: 10px 15px;
  background-color: #17a35e;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.copied-banner {
  margin-top: 20px;
  text-align: center;
  color: #17a35e;
  font-weight: 600;
}
</style>
