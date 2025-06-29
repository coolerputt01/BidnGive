<template>
  <div class="merged-bid-card">
    <div class="header">
      <h3>💼 Bid — ₦{{ bid.amount.toLocaleString() }}</h3>
      <span class="status" :class="bid.status">{{ formatStatus(bid.status) }}</span>
    </div>

    <div class="details">
      <div class="info"><strong>📆 Created:</strong> {{ formatDate(bid.created_at) }}</div>
      <div class="info"><strong>📊 Plan:</strong> {{ bid.plan.replace('_', '% in ') + ' hrs' }}</div>
      <div class="info"><strong>💰 Expected Return:</strong> ₦{{ bid.expected_return.toLocaleString() }}</div>
      <div class="info"><strong>📈 Profit:</strong> ₦{{ profitAmount(bid.amount, bid.expected_return) }}</div>
      <div class="info"><strong>📦 Type:</strong> {{ bid.type === 'investment' ? 'Investment' : 'Withdrawal' }}</div>
      <div class="info" v-if="bid.status === 'merged'"><strong>⏳ Time Left:</strong> {{ timeLeft(bid.merged_at) }}</div>
    </div>

    <div v-if="bid.status === 'merged'" class="participants">
      <h4>📨 Merged With:</h4>
      <ul>
        <li v-for="merge in bid.merges" :key="merge.id">
          <span>{{ merge.user_name }} —
            <a :href="`https://wa.me/${merge.phone}`" target="_blank">WhatsApp</a>
          </span>
        </li>
      </ul>
    </div>

    <div v-if="bid.status === 'merged'" class="actions">
      <input type="file" @change="handleProof" />
      <button @click="submitProof">📤 Submit Payment Proof</button>
    </div>

    <div v-if="bid.status === 'completed' && bid.type !== 'withdrawal'" class="actions">
      <button class="withdraw-btn" @click="withdraw">💸 Withdraw Returns</button>
    </div>
    <!-- Cancel Button -->
    <div v-if="bid.status === 'pending'" class="actions">
      <button class="cancel-btn" @click="cancelBid">❌ Cancel Bid</button>
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
const selectedProof = ref(null)

const formatDate = (iso) => {
  const date = new Date(iso)
  return date.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

const profitAmount = (amount, expected) => {
  return (expected - amount).toLocaleString()
}

const formatStatus = (status) => ({
  pending: '🕒 Awaiting Merge',
  merged: '🔗 Merged, Pay Now',
  paid: '💳 Paid, Awaiting Confirmation',
  completed: '✅ Completed',
  expired: '⌛ Expired'
})[status] || status

const timeLeft = (mergedAt) => {
  const merged = new Date(mergedAt)
  const now = new Date()
  const diff = 5 * 60 * 60 * 1000 - (now - merged)
  if (diff <= 0) return 'Expired'
  const hrs = Math.floor(diff / (1000 * 60 * 60))
  const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  return `${hrs}h ${mins}m remaining`
}

const handleProof = (e) => {
  selectedProof.value = e.target.files[0]
}

const submitProof = async () => {
  if (!selectedProof.value) return toast.error('Select a file.')
  const formData = new FormData()
  formData.append('proof', selectedProof.value)

  try {
    await axios.post(
      `https://bidngive.onrender.com/api/bids/${props.bid.id}/upload-proof/`,
      formData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    toast.success('Proof uploaded.')
    emit('action')
  } catch {
    toast.error('Upload failed.')
  }
}

const withdraw = async () => {
  try {
    await axios.post(
      `https://bidngive.onrender.com/api/bids/withdraw/`,
      { amount: props.bid.amount },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    toast.success('Withdrawal created.')
    emit('action')
  } catch (err) {
    toast.error('Withdrawal failed.')
  }
}
const cancelBid = async () => {
  try {
    await axios.delete(`https://bidngive.onrender.com/api/bids/${props.bid.id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Bid cancelled successfully.')
    emit('action')
  } catch (err) {
    toast.error('Failed to cancel bid.')
  }
}
</script>

<style scoped>
.cancel-btn {
  background-color: #f44336;
}
.cancel-btn:hover {
  background-color: #d32f2f;
}

.merged-bid-card {
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
  color: #fff;
}
.status.pending {
  background-color: #ffc107;
  color: #000;
}
.status.merged {
  background-color: #17a35e;
}
.status.completed {
  background-color: #4caf50;
}
.status.expired {
  background-color: #9e9e9e;
}

.details .info {
  margin: 6px 0;
  font-size: 0.95em;
}

.participants ul {
  list-style: none;
  padding: 0;
  margin: 10px 0;
}
.participants li {
  margin: 6px 0;
}

.actions {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

input[type="file"] {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 8px;
  font-size: 0.95em;
}

button {
  background-color: #17a35e;
  color: white;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #128f4a;
}
.withdraw-btn {
  background-color: #dc3545;
}
.withdraw-btn:hover {
  background-color: #c82333;
}
</style>
