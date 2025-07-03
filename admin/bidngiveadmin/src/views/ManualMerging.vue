<template>
  <main class="manual-merge-container">
    <h1>🔄 Manual Merge Bids</h1>
    <p class="subtitle">
      Select exactly <strong>two pending bids</strong> to merge them manually.
    </p>

    <div v-if="loading" class="loader">Loading bids…</div>

    <div v-else>
      <table class="bids-table" v-if="bids.length">
        <thead>
          <tr>
            <th>Select</th>
            <th>User</th>
            <th>Amount (₦)</th>
            <th>Plan</th>
            <th>Created At</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="bid in bids" :key="bid.id">
            <td>
              <input
                type="checkbox"
                :value="bid.id"
                v-model="selectedBidIds"
                :disabled="isCheckboxDisabled(bid.id)"
                :aria-label="`Select bid ${bid.id}`"
              />
            </td>
            <td>{{ bid.username }}</td>
            <td>{{ formatAmount(bid.amount) }}</td>
            <td>{{ bid.plan }}</td>
            <td>{{ formatDate(bid.created) }}</td>
            <td><span class="status pending">Pending</span></td>
          </tr>
        </tbody>
      </table>

      <div v-else class="empty-message">
        No pending bids found.
      </div>

      <button
        class="merge-button"
        :disabled="selectedBidIds.length !== 2 || merging"
        @click="handleMerge"
        aria-live="polite"
      >
        <span v-if="merging">Merging...</span>
        <span v-else>Merge Selected Bids</span>
      </button>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const bids = ref([])
const selectedBidIds = ref([])
const loading = ref(true)
const merging = ref(false)

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchPendingBids = async () => {
  loading.value = true
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/admin/pending-bids/', { headers })
    bids.value = res.data
  } catch (error) {
    toast.error('Failed to load pending bids.')
  } finally {
    loading.value = false
  }
}

const handleMerge = async () => {
  if (selectedBidIds.value.length !== 2) return

  merging.value = true
  try {
    const res = await axios.post(
      'https://bidngive.onrender.com/api/merge/manual/',
      { bid_ids: selectedBidIds.value },
      { headers }
    )
    toast.success(res.data.message || 'Bids merged successfully.')
    selectedBidIds.value = []
    fetchPendingBids()
  } catch (error) {
    const msg = error.response?.data?.error || 'Failed to merge bids.'
    toast.error(msg)
  } finally {
    merging.value = false
  }
}

const formatDate = (iso) => {
  const d = new Date(iso)
  return d.toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const formatAmount = (num) => {
  return Number(num).toLocaleString('en-NG', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

// Prevent checking more than 2 checkboxes
const isCheckboxDisabled = (bidId) => {
  return selectedBidIds.value.length === 2 && !selectedBidIds.value.includes(bidId)
}

onMounted(() => {
  fetchPendingBids()
})
</script>

<style scoped>
.manual-merge-container {
  max-width: 900px;
  margin: 2rem auto 4rem;
  padding: 1.5rem;
  background: white;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #222;
}

h1 {
  font-weight: 700;
  font-size: 1.8rem;
  color: #17a35e;
  margin-bottom: 0.25rem;
  user-select: none;
}

.subtitle {
  margin-bottom: 1.5rem;
  font-size: 1rem;
  color: #555;
}

.loader {
  text-align: center;
  font-size: 1.1rem;
  color: #888;
  margin: 2rem 0;
}

.bids-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.8rem;
}

.bids-table th,
.bids-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #eee;
  text-align: left;
  vertical-align: middle;
}

.bids-table th {
  background-color: #f0f8f5;
  color: #17a35e;
  font-weight: 700;
  user-select: none;
}

.bids-table tbody tr:hover {
  background-color: #f7fdf8;
}

.status.pending {
  background-color: #fff4ce;
  color: #856404;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
  user-select: none;
  display: inline-block;
}

.merge-button {
  display: block;
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
  padding: 14px 24px;
  background-color: #17a35e;
  border: none;
  border-radius: 28px;
  font-size: 1.1rem;
  font-weight: 700;
  color: white;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.3s ease;
}

.merge-button:disabled {
  background-color: #a2d5a0;
  cursor: not-allowed;
}

.merge-button:not(:disabled):hover {
  background-color: #129045;
}
</style>
