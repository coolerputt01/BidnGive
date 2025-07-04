<template>
  <main class="all-bids-container">
    <h2>📊 All Bids</h2>

    <!-- Filter Buttons -->
    <div class="filter-buttons">
      <button
        v-for="option in filterOptions"
        :key="option"
        :class="{ active: selectedFilter === option }"
        @click="selectedFilter = option"
      >
        {{ option }}
      </button>
    </div>

    <!-- No Bids -->
    <div v-if="filteredBids.length === 0" class="empty">No {{ selectedFilter.toLowerCase() }} bids found.</div>

    <!-- Bids Table -->
    <table v-else class="bids-table">
      <thead>
        <tr>
          <th>User</th>
          <th>Amount</th>
          <th>Plan</th>
          <th>Status</th>
          <th>Created At</th>
          <th>Merged At</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="bid in filteredBids" :key="bid.id">
          <td>{{ bid.username }}</td>
          <td>₦{{ bid.amount.toLocaleString() }}</td>
          <td>{{ bid.plan }}</td>
          <td><span class="status" :class="bid.status">{{ bid.status }}</span></td>
          <td>{{ formatDate(bid.created) }}</td>
          <td>{{ bid.merged_at ? formatDate(bid.merged_at) : '—' }}</td>
          <td>
            <button
              v-if="canCancel(bid.status)"
              class="cancel-btn"
              @click="cancelBid(bid.id)"
            >
              Cancel
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const bids = ref([])
const selectedFilter = ref('All')
const filterOptions = ['All', 'Pending', 'Merged', 'Paid', 'Cancelled']

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchBids = async () => {
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/admin/pending-bids/', { headers })
    bids.value = res.data
    console.log(bids.value)
  } catch (err) {
    toast.error('Failed to fetch bids')
  }
}

const cancelBid = async (bidId) => {
  try {
    await axios.post(
      'https://bidngive.onrender.com/api/admin/cancel-investment/',
      { bid_id: bidId },
      { headers }
    )
    toast.success(`Bid #${bidId} cancelled`)
    fetchBids()
  } catch (err) {
    toast.error(err.response?.data?.error || 'Cancellation failed')
  }
}

const canCancel = (status) => status === 'pending' || status === 'merged'

const filteredBids = computed(() => {
  if (selectedFilter.value === 'All') return bids.value
  return bids.value.filter((b) => b.status.toLowerCase() === selectedFilter.value.toLowerCase())
})

const formatDate = (iso) => {
  const d = new Date(iso)
  return d.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(fetchBids)
</script>

<style scoped>
.all-bids-container {
  max-width: 1000px;
  margin: 40px auto;
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', sans-serif;
}

h2 {
  margin-bottom: 20px;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}
.filter-buttons button {
  padding: 8px 16px;
  border: none;
  background: #f0f0f0;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
.filter-buttons button.active {
  background: #004f28;
  color: white;
}

.bids-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
.bids-table th, .bids-table td {
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
  text-align: left;
  font-size: 0.95rem;
}
.status {
  padding: 4px 10px;
  border-radius: 6px;
  text-transform: capitalize;
  background: #ddd;
}
.status.pending {
  background-color: #ffc107;
  color: #000;
}
.status.merged {
  background-color: #17a35e;
  color: #fff;
}
.status.paid {
  background-color: #4caf50;
  color: #fff;
}
.status.cancelled {
  background-color: #d32f2f;
  color: #fff;
}

.cancel-btn {
  padding: 6px 12px;
  background: #d11a2a;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.cancel-btn:hover {
  background: #a30d1b;
}

.empty {
  font-style: italic;
  color: #888;
  margin-top: 20px;
}
</style>
