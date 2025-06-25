<template>
  <div class="bid-card">
    <div class="card-header">
      <div class="left">
        <h3 class="amount">₦{{ bid.amount.toLocaleString() }}</h3>
        <p class="plan">Plan: {{ bid.plan }}</p>
      </div>
      <span :class="['status-badge', bid.status]">
        {{ bid.status.toUpperCase() }}
      </span>
    </div>

    <hr class="divider" />

    <div class="card-body">
      <div class="info-pair">
        <span class="label">📅 Created:</span>
        <span class="value">{{ formatDate(bid.created_at) }}</span>
      </div>
      <div class="info-pair">
        <span class="label">💸 Expected Return:</span>
        <span class="value">₦{{ calculateReturn(bid.amount, bid.plan) }}</span>
      </div>
      <div class="info-pair">
        <span class="label">⏳ Status:</span>
        <span class="value">
          {{
            bid.status === 'pending' ? 'Awaiting Merge'
            : bid.status === 'merged' ? 'Merged, Awaiting Payment'
            : bid.status === 'paid' ? 'Paid, Awaiting Confirmation'
            : bid.status === 'completed' ? 'Completed'
            : bid.status === 'expired' ? 'Expired'
            : bid.status
          }}
        </span>
      </div>
    </div>

    <div class="card-footer">
      <button
        v-if="bid.status === 'paid' && bid.can_recommit"
        class="btn-primary"
        @click="$emit('action', bid)"
      >
        🔁 Recommit
      </button>

      <button
        v-if="bid.status === 'pending'"
        class="btn-danger"
        @click="cancelBid"
      >
        ❌ Cancel Bid
      </button>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { toast } from 'vue3-toastify'
const props = defineProps({ bid: Object })
const emit = defineEmits(['refresh', 'action'])
const token = localStorage.getItem('access_token')

const formatDate = (isoDate) => {
  const date = new Date(isoDate)
  return date.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

const calculateReturn = (amount, plan) => {
  try {
    const [percent] = plan.split('_')
    const percentValue = parseFloat(percent)
    const profit = (amount * percentValue) / 100
    return (amount + profit).toLocaleString()
  } catch {
    return 'N/A'
  }
}

const cancelBid = async () => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/bids/${props.bid.id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Bid cancelled.')
    emit('refresh')
  } catch {
    toast.error('Failed to cancel bid.')
  }
}
</script>

<style scoped>
.bid-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;
  max-width: 520px;
  margin-inline: auto;
  font-family: 'Segoe UI', sans-serif;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.card-header .left {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.amount {
  font-size: 1.7em;
  font-weight: 700;
  color: #191919;
}

.plan {
  font-size: 0.9em;
  color: #555;
  font-weight: 500;
}

.status-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.75em;
  font-weight: 700;
  text-transform: uppercase;
  color: #fff;
}

.status-badge.pending {
  background-color: #ffc107;
  color: #000;
}

.status-badge.paid {
  background-color: #17a35e;
}

.status-badge.failed {
  background-color: #dc3545;
}

.divider {
  border: none;
  border-top: 1px solid #eee;
  margin: 16px 0;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-bottom: 12px;
}

.info-pair {
  display: flex;
  justify-content: space-between;
  font-size: 0.95em;
}

.label {
  font-weight: 600;
  color: #666;
}

.value {
  font-weight: 500;
  color: #222;
}

.card-footer {
  text-align: right;
  margin-top: 10px;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn-primary {
  background-color: #17a35e;
  color: #fff;
  padding: 10px 22px;
  border-radius: 30px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #128f4a;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  padding: 10px 22px;
  border-radius: 30px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-danger:hover {
  background-color: #c82333;
}
</style>
