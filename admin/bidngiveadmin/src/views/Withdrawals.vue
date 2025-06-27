<template>
  <div class="container">
    <h2>Pending Withdrawals</h2>

    <div v-if="loading" class="loader">Loading...</div>
    <div v-else>
      <table v-if="withdrawals.length" class="table">
        <thead>
          <tr>
            <th>User</th>
            <th>Email</th>
            <th>Amount</th>
            <th>Requested At</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in withdrawals" :key="item.id">
            <td>{{ item.user }}</td>
            <td>{{ item.email }}</td>
            <td>₦{{ item.amount.toLocaleString() }}</td>
            <td>{{ new Date(item.requested_at).toLocaleString() }}</td>
            <td>
              <button @click="markAsPaid(item.id)" class="btn">Mark as Paid</button>
            </td>
          </tr>
        </tbody>
      </table>

      <p v-else>No pending withdrawals at this time.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { toast } from 'vue3-toastify';

const withdrawals = ref([]);
const loading = ref(true);
const baseUrl = 'https://bidngive.onrender.com/api/admin';
const token = localStorage.getItem('access_token');
const headers = { Authorization: `Bearer ${token}` };

const fetchWithdrawals = async () => {
  loading.value = true;
  try {
    const res = await axios.get(`${baseUrl}/withdrawals/pending/`, { headers });
    withdrawals.value = res.data;
  } catch (err) {
    toast.error("Failed to fetch withdrawals.");
  } finally {
    loading.value = false;
  }
};

const markAsPaid = async (id) => {
  try {
    await axios.post(`${baseUrl}/withdrawals/mark-paid/${id}/`, {}, { headers });
    toast.success("Marked as paid.");
    withdrawals.value = withdrawals.value.filter(w => w.id !== id);
  } catch (err) {
    toast.error("Failed to mark as paid.");
  }
};

onMounted(fetchWithdrawals);
</script>

<style scoped>
.container {
  padding: 30px;
  max-width: 1000px;
  margin: auto;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  font-weight: 700;
  color: #222;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 12px;
  border: 1px solid #ccc;
  text-align: left;
}

.table th {
  background-color: #f7f7f7;
}

.btn {
  background-color: #17a35e;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
}

.btn:hover {
  background-color: #138f52;
}

.loader {
  text-align: center;
  font-size: 1.1em;
  color: #888;
}
</style>
