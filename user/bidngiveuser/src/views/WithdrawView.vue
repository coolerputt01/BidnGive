<template>
  <main class="withdraw-history">
    <header class="page-header">
      <h1>💸 Withdrawal History</h1>
      <p>Monitor your past referral and wallet withdrawal activities here. Stay in control of your earnings.</p>
    </header>

    <div v-if="loading" class="loader-wrapper">
      <div class="loader"></div>
    </div>

    <div v-else>
      <div class="filter-tabs">
        <button
          v-for="status in ['all', 'pending', 'completed', 'cancelled']"
          :key="status"
          :class="['filter-btn', { active: selectedStatus === status }]"
          @click="selectedStatus = status"
        >
          {{ status === 'all' ? 'All' : status.charAt(0).toUpperCase() + status.slice(1) }}
        </button>
      </div>

      <div v-if="filteredWithdrawals.length === 0" class="empty-message">
        <img src="/icons/empty-wallet.svg" alt="No Data" class="empty-illustration" />
        <p>No withdrawals in this category.</p>
      </div>

      <section v-else class="history-list">
        <div
          v-for="bid in filteredWithdrawals"
          :key="bid.id"
          class="history-card"
        >
          <div class="card-left">
            <div class="card-amount">
              <span class="label">Amount</span>
              <h3>₦{{ parseFloat(bid.amount).toLocaleString() }}</h3>
            </div>

            <div class="card-status-date">
              <div class="card-status">
                <span class="label">Status</span>
                <span :class="['status-pill', bid.status]">
                  {{ bid.status.toUpperCase() }}
                </span>
              </div>
              <div class="card-date">
                <span class="label">Requested</span>
                <p>{{ formatDate(bid.created_at) }}</p>
              </div>
            </div>
          </div>

          <div class="card-right">
            <div class="ref">
              <span class="label">Reference</span>
              <p>#{{ bid.id }}</p>
            </div>
            <div class="icon-wrapper">
              <i class="fas fa-university"></i>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const withdrawals = ref([])
const loading = ref(true)
const selectedStatus = ref('all')
const token = localStorage.getItem('access_token')

const fetchWithdrawals = async () => {
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/bids/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    withdrawals.value = res.data.filter(bid => bid.type === 'withdrawal')
  } catch (err) {
    toast.error('Unable to load history')
  } finally {
    loading.value = false
  }
}

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

const filteredWithdrawals = computed(() => {
  if (selectedStatus.value === 'all') return withdrawals.value
  return withdrawals.value.filter(w => w.status === selectedStatus.value)
})

onMounted(fetchWithdrawals)
</script>

<style scoped>
.withdraw-history {
  padding: 2em 1.5em 5em;
  background: #f6f8fb;
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
}

.page-header {
  text-align: center;
  margin-bottom: 2em;
}

.page-header h1 {
  font-size: 1.8em;
  font-weight: 700;
  color: #222;
}

.page-header p {
  font-size: 0.95em;
  color: #666;
}

.loader-wrapper {
  display: flex;
  justify-content: center;
  padding: 3em 0;
}

.loader {
  border: 4px solid #ccc;
  border-top: 4px solid #17a35e;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.filter-tabs {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 1.5em;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 6px 14px;
  border-radius: 20px;
  font-weight: 600;
  background: #eee;
  border: none;
  cursor: pointer;
  font-size: 0.85em;
  transition: 0.2s;
}

.filter-btn.active {
  background-color: #17a35e;
  color: white;
}

.empty-message {
  text-align: center;
  margin-top: 3em;
  color: #777;
}

.empty-illustration {
  width: 100px;
  opacity: 0.6;
  margin-bottom: 10px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 700px;
  margin: 0 auto;
}

.history-card {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: #fff;
  padding: 1.2em 1.6em;
  border-radius: 14px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.035);
  gap: 1em;
  transition: 0.2s ease-in-out;
}

.history-card:hover {
  transform: translateY(-2px);
}

.card-left {
  flex: 1;
}

.label {
  font-size: 0.7em;
  font-weight: 600;
  color: #888;
  text-transform: uppercase;
  display: block;
  margin-bottom: 2px;
}

.card-amount h3 {
  margin: 0;
  font-size: 1.4em;
  font-weight: bold;
  color: #111;
}

.card-status-date {
  display: flex;
  gap: 2em;
  margin-top: 10px;
  font-size: 0.85em;
}

.status-pill {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 30px;
  font-size: 0.72em;
  font-weight: 600;
  margin-top: 2px;
}

.status-pill.pending {
  background: #fff4ce;
  color: #856404;
}

.status-pill.completed {
  background: #d4edda;
  color: #155724;
}

.status-pill.cancelled,
.status-pill.expired {
  background: #f8d7da;
  color: #721c24;
}

.card-date p {
  font-size: 0.8em;
  color: #555;
  margin-top: 2px;
}

.card-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-between;
  text-align: right;
}

.ref p {
  font-size: 0.78em;
  color: #666;
}

.icon-wrapper {
  font-size: 1.6em;
  color: #17a35e;
  margin-top: 8px;
}
</style>
