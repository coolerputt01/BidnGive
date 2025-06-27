<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { toast } from 'vue3-toastify';

const email = ref('');
const amount = ref('');
const plan = ref('');
const loading = ref(false);

const token = localStorage.getItem("access_token");
const headers = { Authorization: `Bearer ${token}` };

const createInvestment = async () => {
  if (!email.value || !amount.value || !plan.value) {
    toast.error("Please fill in all fields");
    return;
  }

  loading.value = true;
  try {
    const res = await axios.post(
      'https://bidngive.onrender.com/api/admin/create-investment/',
      { email: email.value, amount: amount.value, plan: '50_24' },
      { headers }
    );
    toast.success(res.data.message);
    email.value = '';
    amount.value = '';
    plan.value = '';
  } catch (err) {
    toast.error(err.response?.data?.error || 'Failed to create investment');
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <main class="investment-container">
    <h2>📥 Create Investment for User</h2>
    <form @submit.prevent="createInvestment" class="investment-form">
      <label>
        User Email:
        <input type="email" v-model="email" required />
      </label>
      <label>
        Amount (₦):
        <input type="number" v-model="amount" required />
      </label>
      <label>
        Plan Name:
        <input type="text" v-model="plan" required placeholder="e.g., Basic / Silver / Gold" />
      </label>
      <button :disabled="loading">
        {{ loading ? 'Processing...' : 'Create Investment' }}
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
input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-top: 6px;
}
button {
  padding: 12px;
  background: #04724D;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
}
button:hover {
  background-color: #03563a;
}
</style>
