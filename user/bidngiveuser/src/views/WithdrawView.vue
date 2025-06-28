<template>
  <main class="withdraw-history">
    <header class="page-header">
      <h2>💸 Withdrawal History</h2>
      <p>Track all your previous withdrawal transactions here.</p>
    </header>

    <div v-if="loading" class="loader-wrapper">
      <div class="loader"></div>
    </div>

    <div v-else-if="withdrawals.length === 0" class="empty-message">
      <p>🚫 No withdrawal records yet.</p>
    </div>

    <section v-else class="history-list">
      <div
        v-for="bid in withdrawals"
        :key="bid.id"
        class="history-card"
      >
        <div class="card-left">
          <h3>₦{{ parseFloat(bid.amount).toLocaleString() }}</h3>
          <p class="small">ID: #{{ bid.id }}</p>
        </div>

        <div class="card-middle">
          <span :class="['status-badge', bid.status]">
            {{ bid.status.toUpperCase() }}
          </span>
          <p class="small">{{ formatDate(bid.created_at) }}</p>
        </div>

        <div class="card-right">
          <i class="fas fa-money-bill-wave fa-lg"></i>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const withdrawals = ref([])
const loading = ref(true)
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

onMounted(fetchWithdrawals)
</script>

<style scoped>
.withdraw-history {
  padding: 20px;
  font-family: 'Segoe UI', sans-serif;
  background: #f8f9fb;
  min-height: 100vh;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h2 {
  font-size: 1.9em;
  font-weight: 700;
  color: #222;
}

.page-header p {
  color: #666;
  font-size: 0.95em;
}

.loader-wrapper {
  display: flex;
  justify-content: center;
  padding: 40px;
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
  to {
    transform: rotate(360deg);
  }
}

.empty-message {
  text-align: center;
  font-size: 1.1em;
  color: #777;
  margin-top: 50px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 650px;
  margin: 0 auto;
}

.history-card {
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
}

.history-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}

.card-left h3 {
  margin: 0;
  font-size: 1.4em;
  font-weight: 700;
  color: #191919;
}

.card-left .small {
  font-size: 0.8em;
  color: #777;
  margin-top: 4px;
}

.card-middle {
  text-align: center;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75em;
  font-weight: bold;
  color: #fff;
  display: inline-block;
  margin-bottom: 4px;
}

.status-badge.pending {
  background-color: #ffc107;
  color: #000;
}

.status-badge.completed {
  background-color: #28a745;
}

.status-badge.cancelled,
.status-badge.expired {
  background-color: #dc3545;
}

.card-middle .small {
  font-size: 0.75em;
  color: #666;
}

.card-right i {
  color: #17a35e;
}
</style>
