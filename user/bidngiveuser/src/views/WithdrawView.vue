<template>
  <main class="withdraw-page">
    <section class="header">
      <h2>Withdraw Funds</h2>
      <p>Enter your details to withdraw to your bank account</p>
    </section>

    <form class="withdraw-form" @submit.prevent="submitWithdrawal">
      <label>
        Bank Name
        <input type="text" v-model="form.bank" placeholder="e.g. Access Bank" />
      </label>

      <label>
        Account Number
        <input type="text" v-model="form.account" maxlength="10" placeholder="e.g. 0123456789" />
      </label>

      <label>
        Amount to Withdraw (₦)
        <input type="number" v-model="form.amount" min="1000" placeholder="e.g. 5000" />
      </label>

      <button type="submit" class="btn" :disabled="loading" style="display: flex;justify-content: center;align-items: center;">
        <span v-if="!loading">Withdraw</span>
        <div v-else class="loader"></div>
      </button>
    </form>

    <div v-if="submitted" class="success-message">
      ✅ Withdrawal request submitted successfully!
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const form = ref({
  bank: '',
  account: '',
  amount: ''
})

const submitted = ref(false)
const loading = ref(false)
const token = localStorage.getItem('access_token') // Or pull from your store

const submitWithdrawal = async () => {
  submitted.value = false
  loading.value = true

  try {
    // Send form data to the backend
    const response = await axios.post(
      'http://127.0.0.1:8000/api/referral/withdraw/', // Your real withdrawal endpoint
      {
        bank: form.value.bank,
        account: form.value.account,
        amount: form.value.amount
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    submitted.value = true
    toast.success(response.data.message || 'Withdrawal request submitted.')

    form.value = { bank: '', account: '', amount: '' }

    setTimeout(() => {
      submitted.value = false
    }, 3000)
  } catch (err) {
    toast.error(err.response?.data?.message || 'Withdrawal failed')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.withdraw-page {
  background-color: #f9f9f9;
  min-height: 100vh;
  padding: 20px;
  font-family: Arial, sans-serif;
  overflow: hidden;
}
.loader {
  border: 3px solid rgb(172, 172, 172); /* Light grey */
  border-top: 3px solid #fff; /* Blue */
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 2s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h2 {
  font-size: 1.8em;
  font-weight: 700;
  color: #191919;
}

.header p {
  font-size: 0.95em;
  color: #555;
}

.withdraw-form {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  max-width: 500px;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
  overflow: hidden;
}

.withdraw-form label {
  display: flex;
  flex-direction: column;
  font-weight: 600;
  color: #333;
}

.withdraw-form input {
  margin-top: 6px;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1em;
}

.btn {
  background-color: #17a35e;
  color: #fff;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #128f4a;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.success-message {
  text-align: center;
  margin-top: 20px;
  font-weight: 600;
  color: #17a35e;
  font-size: 1em;
}
</style>
