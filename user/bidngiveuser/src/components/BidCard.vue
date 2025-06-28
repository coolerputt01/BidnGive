<template>
  <div class="merged-bid-card">
    <div class="header">
      <h3>Merged Bid — ₦{{ bid.amount.toLocaleString() }}</h3>
      <span class="status" :class="bid.status">{{ formatStatus(bid.status) }}</span>
    </div>

    <div class="details">
      <p><strong>Created:</strong> {{ formatDate(bid.created_at) }}</p>
      <p><strong>Plan:</strong> {{ bid.plan }}</p>
      <p><strong>Expected Return:</strong> ₦{{ calculateReturn(bid.amount, bid.plan) }}</p>
    </div>

    <div v-if="bid.status === 'merged'" class="participants">
      <h4>📨 You’ve been merged with:</h4>
      <ul>
        <li v-for="merge in bid.merges" :key="merge.id">
          <span>{{ merge.user_name }} —
            <a :href="`https://wa.me/${merge.phone}`" target="_blank">WhatsApp</a>
          </span>
        </li>
      </ul>
    </div>

    <!-- Upload proof if merged -->
    <div v-if="bid.status === 'merged'" class="actions">
      <input type="file" @change="handleProof" />
      <button @click="submitProof">📤 Submit Payment Proof</button>
    </div>

    <!-- Withdraw if completed (not withdrawal bid) -->
    <div v-if="bid.status === 'completed' && bid.type !== 'withdrawal'" class="actions">
      <button class="withdraw-btn" @click="withdraw">💸 Withdraw Returns</button>
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

const calculateReturn = (amount, plan) => {
  try {
    const percent = parseFloat(plan.split('_')[0])
    const profit = (amount * percent) / 100
    return (amount + profit).toLocaleString()
  } catch {
    return 'N/A'
  }
}

const formatStatus = (status) => ({
  pending: 'Awaiting Merge',
  merged: 'Merged, Awaiting Payment',
  paid: 'Paid, Awaiting Confirmation',
  completed: 'Completed',
  expired: 'Expired'
})[status] || status

const handleProof = (e) => {
  selectedProof.value = e.target.files[0]
}

const submitProof = async () => {
  if (!selectedProof.value) return toast.error('Please select a file.')

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
    emit('action')  // notify parent to refetch bids
  } catch {
    toast.error('Failed to upload proof.')
  }
}

const withdraw = async () => {
  try {
    await axios.post(
      `https://bidngive.onrender.com/api/bids/withdraw/`,
      { amount: props.bid.amount },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    toast.success('Withdrawal bid created.')
    emit('action')  // notify parent to refetch bids
  } catch (err) {
    toast.error('Withdrawal failed.')
  }
}
</script>

<style scoped>
.merged-bid-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  max-width: 600px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status {
  padding: 5px 12px;
  border-radius: 20px;
  font-weight: bold;
  color: white;
}

.status.pending {
  background-color: #ffc107;
  color: black;
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

.details p {
  margin: 6px 0;
}

.participants ul {
  list-style: none;
  padding: 0;
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
  padding: 8px;
  border-radius: 8px;
}

button {
  background-color: #17a35e;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
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
