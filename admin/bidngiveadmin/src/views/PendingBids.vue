<template>
  <main class="container">
    <h2 class="title">Pending Bids</h2>

    <div class="bids-table" v-if="bids.length">
      <table>
        <thead>
          <tr>
            <th>User</th>
            <th>Amount</th>
            <th>Plan</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="bid in bids" :key="bid.id">
            <td>{{ bid.username }}</td>
            <td>₦{{ bid.amount.toLocaleString() }}</td>
            <td>{{ bid.plan }}</td>
            <td>{{ formatDate(bid.created) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="no-bids">No pending bids in auction room currently.</p>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { toast } from 'vue3-toastify';

const bids = ref([]);
const baseUrl = 'https://bidngive.onrender.com';

const fetchPendingBids = async () => {
  try {
    const token = localStorage.getItem('access_token');
    const res = await axios.get(`${baseUrl}/api/admin/pending-bids/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    bids.value = res.data;
    console.log(bids.value)
  } catch (err) {
    console.error('Failed to fetch pending bids', err);
    toast.error('Could not load pending bids');
  }
};

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleString();
};

onMounted(fetchPendingBids);
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 40px auto;
  padding: 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  font-family: 'Segoe UI', sans-serif;
}

.title {
  text-align: center;
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 30px;
}

.bids-table table {
  width: 100%;
  border-collapse: collapse;
}

.bids-table th,
.bids-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.bids-table th {
  background: #f5f5f5;
  font-weight: 600;
}

.no-bids {
  text-align: center;
  color: #777;
  margin-top: 40px;
  font-size: 1rem;
}
</style>
