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
    const res = await axios.get('https://bidngive.onrender.com/api/acccounts/me/', {
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
