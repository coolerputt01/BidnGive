<template>
  <section class="create-bid-page">
    <section class="header">
      <h2>Create a New Investment Bid</h2>
      <p>Set the amount, duration, and reward percentage</p>
    </section>

    <div style="text-align: center; display: flex; justify-content: center; align-items: center; border-radius: 3px;">
      <span style="color: #004f28; background-color: #e0ffe0; font-size: 0.9em; padding: 4px; font-weight: 600; border-radius: 6px;">
        ⏰ Next auction starts in 0h :01m :0s
      </span>
    </div>

    <section class="info-banner">
      💡 Create a bid and let others invest with you. You'll pay back with a percentage reward.
    </section>

    <section class="create-section">
      <form class="create-form" @submit.prevent="submitBid">
        <label>
          Amount to Receive (₦):
          <input type="number" v-model="form.amount" required />
        </label>
        <label>
          Duration (days):
          <input type="number" v-model="form.duration" required />
        </label>
        <label>
          Return Percentage (%):
          <input type="number" v-model="form.return" required />
        </label>
        <button type="submit" class="btn-join">Create Bid</button>
      </form>
    </section>
  </section>
</template>

<script setup>
import { ref } from 'vue';

const form = ref({
  amount: '',
  duration: '',
  return: ''
});

const submitBid = () => {
  alert(`Bid created for ₦${form.value.amount}, ${form.value.return}% return in ${form.value.duration} days.`);
  form.value = { amount: '', duration: '', return: '' };
};
</script>

<style scoped>
.create-bid-page {
  background-color: #f4f4f4;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 20px;
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

.info-banner {
  background-color: #e0ffe0;
  padding: 12px;
  border-left: 5px solid #17a35e;
  font-size: 0.9em;
  color: #004f28;
  margin: 20px 0;
  border-radius: 6px;
}

.create-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.create-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.create-form label {
  display: flex;
  flex-direction: column;
  font-weight: 600;
  color: #333;
}

.create-form input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-top: 5px;
}

.btn-join {
  padding: 10px;
  width: 100%;
  background-color: #17a35e;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-join:hover {
  background-color: #128f4a;
}
</style>
