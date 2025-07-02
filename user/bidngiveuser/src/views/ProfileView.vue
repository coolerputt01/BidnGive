<template>
  <main class="profile-page" style="padding-bottom: 5%;">
    <!-- Header -->
    <section class="profile-header">
      <img src="/icons/profile.svg" alt="Profile" class="profile-avatar" />
      <h2>{{ user.full_name }}</h2>
      <p>{{ user.email }}</p>
    </section>

    <!-- User Info Card -->
    <section class="profile-details" v-if="!loading">
      <div class="detail-item">
        <label>Username</label>
        <input type="text" v-model="user.username" disabled />
      </div>

      <div class="detail-item">
        <label>Email</label>
        <input type="email" v-model="user.email" disabled />
      </div>

      <div class="detail-item">
        <label>Phone Number</label>
        <input type="tel" v-model="user.phone_number" disabled />
      </div>

      <div class="detail-item">
        <label>Referral Code</label>
        <div class="referral-box">
          <input type="text" :value="user.referral_code" readonly />
          <button @click="copyReferral">Copy</button>
        </div>
      </div>
    </section>

    <!-- Bank Account Info Card -->
    <section class="bank-details-card" v-if="!loading">
      <h3 style="margin-bottom: 20px;">🏦 Bank Account Details</h3>
      <div class="detail-item">
        <label>Account Number</label>
        <input type="text" v-model="account.account_number" placeholder="Enter your account number" />
      </div>

      <div class="detail-item">
        <label>Bank Name</label>
        <input type="text" v-model="account.bank_name" placeholder="Enter your bank name" />
      </div>

      <button class="save-btn" @click="saveBankDetails">💾 Save Changes</button>
    </section>

    <div v-if="copied" class="copied-banner">Copied to clipboard ✅</div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const token = localStorage.getItem('access_token')
const user = ref({})
const account = ref({ account_number: '', bank_name: '' })
const loading = ref(true)
const copied = ref(false)

const fetchProfile = async () => {
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/accounts/me/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = res.data
    account.value.account_number = res.data.account_number || ''
    account.value.bank_name = res.data.bank_name || ''
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

const saveBankDetails = async () => {
  try {
    await axios.patch('https://bidngive.onrender.com/api/accounts/me/', account.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Bank details updated ✅')
  } catch (err) {
    toast.error('Failed to update bank info ❌')
  }
}

onMounted(fetchProfile)
</script>

<style scoped>
.profile-page {
  padding: 30px 20px;
  background-color: #f5f5f5;
  font-family: Arial, sans-serif;
  min-height: 100vh;
  box-sizing: border-box;
}

.profile-header {
  text-align: center;
  margin-bottom: 25px;
  padding: 0 20px;
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

.profile-details,
.bank-details-card {
  background-color: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  max-width: 540px;
  margin: 0 auto 30px;
  box-sizing: border-box;
}

.detail-item {
  margin-bottom: 18px;
}

.detail-item label {
  font-weight: 600;
  display: block;
  margin-bottom: 8px;
  color: #333;
}

.detail-item input {
  width: 100%;
  padding: 14px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1em;
  box-sizing: border-box;
}

.referral-box {
  display: flex;
  gap: 10px;
}

.referral-box input {
  flex: 1;
}

.referral-box button,
.save-btn {
  padding: 14px 20px;
  background-color: #17a35e;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1em;
}

.save-btn:hover,
.referral-box button:hover {
  background-color: #128f4a;
}

.copied-banner {
  margin-top: 20px;
  text-align: center;
  color: #17a35e;
  font-weight: 600;
}
</style>
