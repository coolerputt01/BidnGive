<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { toast } from 'vue3-toastify';

const bids = ref([]);
const loading = ref(false);

const token = localStorage.getItem("access_token");
const headers = { Authorization: `Bearer ${token}` };

const fetchBids = async () => {
  try {
    const res = await axios.get("https://bidngive.onrender.com/api/admin/pending-bids/", { headers });
    bids.value = res.data;
    console.log(bids.value)
  } catch (err) {
    toast.error("Failed to fetch bids");
  }
};

const cancelBid = async (bidId) => {
  try {
    await axios.post(
      "https://bidngive.onrender.com/api/admin/cancel-investment/",
      { bid_id: bidId },
      { headers }
    );
    toast.success(`Bid #${bidId} cancelled`);
    fetchBids(); // Refresh
  } catch (err) {
    toast.error(err.response?.data?.error || "Cancellation failed");
  }
};

onMounted(fetchBids);
</script>

<template>
  <main class="cancel-container">
    <h2>❌ Cancel Recommitment</h2>
    <div v-if="bids.length === 0" class="empty">No active recommitment found.</div>
    <table v-else class="bid-table">
      <thead>
        <tr>
          <th>User</th>
          <th>Amount</th>
          <th>Plan</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="bid in bids" :key="bid.id">
          <td>{{ bid.username }}</td>
          <td>₦{{ bid.amount.toLocaleString() }}</td>
          <td>{{ bid.plan }}</td>
          <td><span class="status">{{ bid.status }}</span></td>
          <td>
            <button class="cancel-btn" @click="cancelBid(bid.id)">
              Cancel
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </main>
</template>

<style scoped>
.cancel-container {
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.bid-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.bid-table th, .bid-table td {
  border-bottom: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}
.cancel-btn {
  padding: 6px 14px;
  background: #d11a2a;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.cancel-btn:hover {
  background: #a30d1b;
}
.status {
  padding: 4px 8px;
  border-radius: 4px;
  background: #f0f0f0;
}
.empty {
  margin-top: 20px;
  font-style: italic;
  color: gray;
}
</style>
