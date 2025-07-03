<template>
  <div class="bid-card">
    <div class="bid-header">
      <div>
        <h3 class="amount">₦{{ bid.amount.toLocaleString() }}</h3>
        <p class="plan">{{ bid.plan.replace('_', '% in ') }} hrs</p>
      </div>
      <span class="status" :class="bid.status">{{ formatStatus(bid.status) }}</span>
    </div>

    <div class="bid-body">
      <div class="info">
        <strong>Expected Return:</strong>
        <span>₦{{ bid.expected_return.toLocaleString() }}</span>
      </div>
      <div class="info">
        <strong>Type:</strong>
        <span class="capitalize">{{ bid.type }}</span>
      </div>
      <div class="info">
        <strong>Status:</strong>
        <span class="capitalize">{{ bid.status }}</span>
      </div>

      <!-- ❗ Not verified notice -->
      <div
        v-if="bid.status === 'paid' && !bid.receiver_confirmed"
        class="not-verified"
      >
        ❗ Payment not verified by receiver yet.
      </div>
    </div>

    <div class="bid-actions">
      <!-- Cancel button only for pending bids -->
      <button
        v-if="canCancel"
        class="btn cancel-btn"
        :disabled="loading"
        @click="cancelBid"
      >
        <span v-if="loading">⏳ Cancelling...</span>
        <span v-else>❌ Cancel</span>
      </button>

      <button
        v-if="bid.status === 'paid' && bid.receiver_confirmed"
        class="btn recommit-btn"
        @click="recommit"
      >
        🔁 Recommit
      </button>
      <button
        v-if="bid.status === 'paid' && bid.receiver_confirmed"
        class="btn withdraw-btn"
        @click="withdraw"
      >
        💸 Withdraw
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const props = defineProps({ bid: Object })
const emit = defineEmits(['action'])
const token = localStorage.getItem('access_token')

const loading = ref(false)

const formatStatus = (status) => ({
  pending: '🕒 Pending',
  merged: '🔗 Merged',
  paid: '💳 Paid',
  completed: '✅ Completed',
  expired: '⌛ Expired',
  cancelled: '❌ Cancelled'
})[status] || status

const canCancel = props.bid.status === 'pending'

const cancelBid = async () => {
  loading.value = true
  try {
    await axios.delete(`https://bidngive.onrender.com/api/bids/${props.bid.id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Bid cancelled successfully.')
    emit('action')
  } catch (err) {
    toast.error('Failed to cancel bid.')
  } finally {
    loading.value = false
  }
}

const recommit = async () => {
  try {
    await axios.post(
      `https://bidngive.onrender.com/api/bids/`,
      {
        amount: props.bid.amount,
        plan: props.bid.plan,
        type: 'investment'
      },
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    )
    toast.success('Recommit successful')
    emit('action')
  } catch {
    toast.error('Recommit failed')
  }
}

const withdraw = async () => {
  try {
    await axios.post(
      `https://bidngive.onrender.com/api/bids/withdraw/`,
      {
        amount: props.bid.amount
      },
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    )
    toast.success('Withdrawal successful')
    emit('action')
  } catch {
    toast.error('Withdrawal failed')
  }
}
</script>

<style scoped>
.bid-card {
  background: #ffffff;
  border-radius: 18px;
  padding: 24px;
  max-width: 620px;
  margin: 20px auto;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
  font-family: 'Segoe UI', sans-serif;
  transition: transform 0.2s ease;
}
.bid-card:hover {
  transform: translateY(-2px);
}
.bid-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.amount {
  font-size: 1.5rem;
  color: #0c69c8;
  margin: 0;
}
.plan {
  color: #888;
  font-size: 0.9rem;
  margin-top: 4px;
}
.status {
  padding: 6px 14px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.85rem;
  color: white;
  text-transform: uppercase;
}
.status.pending {
  background-color: #ffc107;
  color: #000;
}
.status.merged {
  background-color: #2196f3;
}
.status.paid {
  background-color: #4caf50;
}
.status.completed {
  background-color: #2e7d32;
}
.status.expired {
  background-color: #9e9e9e;
}
.status.cancelled {
  background-color: #d32f2f;
}
.bid-body {
  margin-top: 20px;
}
.info {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 0.95rem;
}
.capitalize {
  text-transform: capitalize;
}
.bid-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
}
.btn {
  padding: 12px 20px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 0.95rem;
}
.cancel-btn {
  background-color: #d32f2f;
  color: white;
}
.cancel-btn:hover {
  background-color: #b71c1c;
}
.recommit-btn {
  background-color: #0c69c8;
  color: white;
}
.recommit-btn:hover {
  background-color: #0758a0;
}
.withdraw-btn {
  background-color: #dc2626;
  color: white;
}
.withdraw-btn:hover {
  background-color: #b91c1c;
}

.not-verified {
  margin-top: 12px;
  padding: 10px;
  background-color: #fff3cd;
  border: 1px solid #ffeeba;
  border-radius: 8px;
  color: #856404;
  font-size: 0.9rem;
  text-align: center;
}
</style>
