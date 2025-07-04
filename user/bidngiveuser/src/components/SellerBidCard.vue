<template>
  <div class="seller-bid-card" v-if="bid">
    <div class="header">
      <h3>💼 Withdrawal — ₦{{ bid.amount.toLocaleString() }}</h3>
      <span class="status" :class="['status', bid.status]">{{ formatStatus(bid.status) }}</span>
    </div>

    <div class="details">
      <div class="info"><strong>📆 Created:</strong> {{ formatDate(bid.created_at) }}</div>
      <div class="info"><strong>💰 Expected Payout:</strong> ₦{{ bid.expected_return.toLocaleString() }}</div>
      <div class="info" v-if="bid.status === 'merged'">
        <strong>⏳ Time Left:</strong> {{ timeLeft(bid.merged_at) }}
      </div>

    </div>
    <div v-if="bid.status === 'completed'" class="completed-msg">
      ✅ This withdrawal has been completed.
    </div>


    <div v-if="bid.status === 'merged' && bid.counterparty_name" class="counterparty">
      <h4>👤 Buyer Details</h4>
      <p><strong>Name:</strong> {{ bid.counterparty_name }}</p>
      <p>
        <strong>Phone:</strong>
        <a :href="`https://wa.me/${bid.counterparty_phone}`" target="_blank" rel="noopener noreferrer">
          {{ bid.counterparty_phone }}
        </a>
      </p>
      <p><strong>Bank:</strong> {{ bid.counterparty_bank || 'N/A' }}</p>
      <p><strong>Account Number:</strong> {{ bid.counterparty_account || 'N/A' }}</p>
      <p><strong>Account Name:</strong> {{ bid.counterparty_account_name || 'N/A' }}</p>
    </div>

    <div v-if="bid.status === 'merged'" class="payment-proof">
      <h4>📎 Payment Proof</h4>
      <div v-if="bid.payment_proof">
        <img :src="bid.payment_proof" alt="Proof" class="proof-img" />
      </div>
      <div v-else>
        <p>No payment proof uploaded yet.</p>
      </div>
      <button @click="confirmPayment" class="confirm-btn">✅ Confirm Payment</button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const props = defineProps({
  bid: {
    type: Object,
    required: true
  }
})
const emit = defineEmits(['action'])

const token = localStorage.getItem('access_token')

const formatDate = (iso) => {
  if (!iso) return 'N/A'
  return new Date(iso).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

const formatStatus = (status) =>
  ({
    pending: '🕒 Awaiting Merge',
    merged: '💸 Awaiting Payment',
    paid: '💳 Paid by Buyer',
    confirmed: '✅ Confirmed',
    completed: '✅ Completed',
    expired: '⌛ Expired',
    cancelled: '❌ Cancelled'
  }[status] || status?.toUpperCase() || 'UNKNOWN')

const timeLeft = (mergedAt) => {
  if (!mergedAt) return 'N/A'
  const merged = new Date(mergedAt)
  const now = new Date()
  const diff = 5 * 60 * 60 * 1000 - (now - merged)
  if (diff <= 0) return 'Expired'
  const hrs = Math.floor(diff / (1000 * 60 * 60))
  const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  return `${hrs}h ${mins}m remaining`
}

const confirmPayment = async () => {
  try {
    await axios.post(
      `https://bidngive.onrender.com/api/bids/confirm-receive/${props.bid.id}/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    toast.success('✅ Payment confirmed.')
    emit('action')
  } catch (err) {
    console.error(err)
    toast.error(err.response?.data?.error || '❌ Confirmation failed.')
  }
}

</script>

<style scoped>
.seller-bid-card {
  background: #fff;
  padding: 22px;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  max-width: 620px;
  margin: 24px auto;
  font-family: 'Segoe UI', sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.status {
  padding: 6px 14px;
  border-radius: 18px;
  font-size: 0.85em;
  font-weight: bold;
  text-transform: uppercase;
  color: #fff;
}
.completed-msg {
  margin-top: 16px;
  padding: 12px;
  background-color: #e6f4ea;
  border-left: 4px solid #2e7d32;
  color: #2e7d32;
  font-weight: 500;
  border-radius: 8px;
}


/* Default status color (if class is missing) */
.status:not(.pending):not(.merged):not(.confirmed):not(.expired):not(.cancelled) {
  background-color: #666;
}

/* Specific status styles */
.status.pending {
  background-color: #ffc107;
  color: #000;
}
.status.merged {
  background-color: #17a35e;
}
.status.confirmed {
  background-color: #4caf50;
}
.status.completed {
  background-color: #2e7d32; /* Darker green */
}
.status.expired {
  background-color: #9e9e9e;
}
.status.cancelled {
  background-color: #d32f2f;
}

.details .info {
  margin: 6px 0;
  font-size: 0.95em;
}

.counterparty,
.payment-proof {
  margin-top: 20px;
}

.proof-img {
  max-width: 100%;
  border-radius: 8px;
  margin-bottom: 10px;
}

.confirm-btn {
  background-color: #17a35e;
  color: white;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 10px;
}
.confirm-btn:hover {
  background-color: #128f4a;
}
</style>
