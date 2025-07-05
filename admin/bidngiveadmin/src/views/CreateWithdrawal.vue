<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const email = ref('')
const amount = ref('')
const plan = ref('50_24')
const loading = ref(false)

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const createWithdrawal = async () => {
  if (!email.value || !amount.value || !plan.value) {
    toast.error('Please fill in all fields')
    return
  }

  const amt = parseFloat(amount.value)
  if (isNaN(amt) || amt < 10000) {
    toast.error('Amount must be at least ₦10,000')
    return
  }

  loading.value = true
  try {
    const res = await axios.post(
      'https://bidngive.onrender.com/api/admin/create-investment/',
      {
        email: email.value,
        amount: amt,
        plan: plan.value,
        type: 'withdrawal',
        expected_return: Math.round(amt * 1.5),
        status: "awaiting",
      },
      { headers }
    )
    toast.success(res.data.message || '✅ Withdrawal bid created (pending auction)')
    email.value = ''
    amount.value = ''
    plan.value = '50_24'
  } catch (err) {
    toast.error(err.response?.data?.error || '❌ Failed to create withdrawal bid')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="investment-container">
    <h2>📤 Create Withdrawal Bid for User</h2>
    <form @submit.prevent="createWithdrawal" class="investment-form">
      <label>
        User Email:
        <input type="email" v-model="email" required />
      </label>

      <label>
        Amount (₦):
        <input type="number" v-model="amount" min="10000" required />
      </label>

      <label>
        Plan:
        <select v-model="plan" required>
          <option value="50_24">50% in 24 hours</option>
        </select>
      </label>

      <button :disabled="loading">
        {{ loading ? 'Creating...' : 'Create Withdrawal' }}
      </button>
    </form>
  </main>
</template>

<style scoped>
.investment-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.investment-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
label {
  display: flex;
  flex-direction: column;
  font-weight: 600;
  color: #333;
}
input,
select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-top: 6px;
}
button {
  padding: 12px;
  background: #95190C;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
}
button:hover {
  background-color: #701408;
}
</style>
