<template>
  <main class="withdraw-page">
    <section class="header">
      <h2>Withdraw Funds</h2>
      <p>Enter your details to withdraw to your bank account</p>
    </section>

    <form class="withdraw-form" @submit.prevent="submitWithdrawal">
      <label>
        Bank Name
        <input type="text" v-model="form.bank" required placeholder="e.g. Access Bank" />
      </label>

      <label>
        Account Number
        <input type="text" v-model="form.account" required maxlength="10" placeholder="e.g. 0123456789" />
      </label>

      <label>
        Amount to Withdraw (₦)
        <input type="number" v-model="form.amount" required min="1000" placeholder="e.g. 5000" />
      </label>

      <button type="submit" class="btn">Withdraw</button>
    </form>

    <div v-if="submitted" class="success-message">
      ✅ Withdrawal request submitted successfully!
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';

const form = ref({
  bank: '',
  account: '',
  amount: ''
});

const submitted = ref(false);

const submitWithdrawal = () => {
  // Example: Validate or send to server
  submitted.value = true;
  setTimeout(() => {
    submitted.value = false;
  }, 3000);
  form.value = { bank: '', account: '', amount: '' };
};
</script>

<style scoped>
.withdraw-page {
  background-color: #f9f9f9;
  min-height: 100vh;
  padding: 20px;
  font-family: Arial, sans-serif;
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

.success-message {
  text-align: center;
  margin-top: 20px;
  font-weight: 600;
  color: #17a35e;
  font-size: 1em;
}
</style>
