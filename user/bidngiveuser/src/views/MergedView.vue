<template>
  <main class="merge-info-page">
    <section class="header">
      <h2>Merged Bids</h2>
      <p>Below are your active merges. Please take necessary action within 5 hours of merging.</p>
    </section>

    <div v-if="bids.length" class="bids-container">
      <div v-for="bid in bids" :key="bid.id" class="bid-card">
        <!-- BID DETAILS -->
        <div class="details-grid">
          <div class="info-row">
            <span class="label">Amount</span>
            <span class="value amount">₦{{ Number(bid.amount).toLocaleString() }}</span>
          </div>
          <div class="info-row">
            <span class="label">Expected Return</span>
            <span class="value">₦{{ Number(bid.expected_return).toLocaleString() }}</span>
          </div>
          <div class="info-row">
            <span class="label">Status</span>
            <span class="value status" :class="bid.status">{{ bid.status.toUpperCase() }}</span>
          </div>
          <div class="info-row">
            <span class="label">Time Left</span>
            <span class="value countdown">{{ countdowns[bid.id] || 'Loading...' }}</span>
          </div>
        </div>

        <p class="warning" v-if="countdowns[bid.id]?.includes('Expired')">
          ⚠️ Your account may be suspended for missing this deadline.
        </p>

        <!-- RECEIVER INFO -->
        <div class="receiver-box">
          <h4>{{ bid.role === 'buyer' ? 'Pay To' : 'From' }} Details</h4>
          <p>
            <strong>Phone:</strong>
            <a :href="whatsappLink(bid.counterparty_phone)" target="_blank" class="whatsapp-link">
              {{ bid.counterparty_phone }}
              <img src="/icons/whatsapp.svg" alt="WhatsApp" class="wa-icon" />
            </a>
          </p>
          <p v-if="bid.counterparty_account">
            <strong>Bank:</strong> {{ bid.counterparty_bank }}
          </p>
          <p v-if="bid.counterparty_account">
            <strong>Account No:</strong> {{ bid.counterparty_account }}
          </p>
          <p v-if="bid.counterparty_account_name">
            <strong>Account Name:</strong> {{ bid.counterparty_account_name }}
          </p>
        </div>

        <!-- BUYER: Upload Payment -->
        <div v-if="bid.role === 'buyer' && bid.status === 'merged'" class="upload-section">
          <label>Upload Payment Proof:</label>
          <input type="file" @change="e => handleFileChange(e, bid.id)" accept="image/*" />

          <div v-if="previewUrl(bid.id)">
            <img :src="previewUrl(bid.id)" class="preview" />
          </div>

          <div v-else-if="bid.payment_proof">
            <img :src="bid.payment_proof" class="preview" />
          </div>

          <button class="btn" @click="() => uploadProof(bid.id)" :disabled="uploadingMap[bid.id]">
            {{ uploadingMap[bid.id] ? 'Uploading...' : 'Submit Payment Proof' }}
          </button>
        </div>

        <!-- SELLER: Confirm Payment -->
        <div v-if="bid.role === 'seller'" class="confirm-section">
          <p class="info-text">
            <strong>Payment Status:</strong>
            <span v-if="bid.status === 'merged'">Waiting for buyer to upload proof.</span>
            <span v-else-if="bid.status === 'paid' && !bid.receiver_confirmed">Proof uploaded. Please confirm receipt.</span>
            <span v-else-if="bid.status === 'paid' && bid.receiver_confirmed">✅ Payment confirmed.</span>
          </p>

          <div v-if="bid.payment_proof && !bid.receiver_confirmed">
            <img :src="bid.payment_proof" class="preview" />
            <button class="btn confirm-btn" @click="() => confirmAsReceiver(bid.id)" :disabled="confirmingMap[bid.id]">
              {{ confirmingMap[bid.id] ? 'Confirming...' : 'Confirm Payment Received' }}
            </button>
          </div>
        </div>

        <!-- BUYER SUCCESS MSG -->
        <div v-if="bid.role === 'buyer' && bid.status === 'paid' && bid.receiver_confirmed" class="success-msg">
          ✅ Payment has been confirmed by the receiver.
        </div>

        <!-- RECOMMIT & WITHDRAW -->
        <div v-if="bid.status === 'paid' && bid.receiver_confirmed" class="actions-buttons">
          <button class="btn recommit-btn" @click="recommit(bid)">🔁 Recommit</button>
          <button class="btn withdraw-btn" @click="withdraw(bid)">💸 Withdraw</button>
        </div>
      </div>
    </div>

    <div v-else class="loading">No merged bids found.</div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const token = localStorage.getItem('access_token')
const bids = ref([])
const countdowns = ref({})
const fileMap = ref({})
const uploadingMap = ref({})
const confirmingMap = ref({})

const previewUrl = (bidId) => {
  const file = fileMap.value[bidId]
  return file ? URL.createObjectURL(file) : null
}


const fetchBids = async () => {
  try {
    const res = await axios.get(`https://bidngive.onrender.com/api/bids/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    bids.value = res.data.filter(b => b.status === 'merged' || b.status === 'paid')
    console.log(bids.value)
    startCountdowns()
  } catch {
    toast.error('Failed to load bids')
  }
}

const handleFileChange = (e, bidId) => {
  fileMap.value[bidId] = e.target.files[0]
}

const uploadProof = async (bidId) => {
  const file = fileMap.value[bidId]
  if (!file) return toast.error('Select a payment proof file')
  uploadingMap.value[bidId] = true

  const formData = new FormData()
  formData.append('payment_proof', file)

  try {
    await axios.put(`https://bidngive.onrender.com/api/bids/upload-proof/${bidId}/`, formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    toast.success('Proof uploaded successfully')
    fetchBids()
  } catch {
    toast.error('Upload failed')
  } finally {
    uploadingMap.value[bidId] = false
  }
}

const confirmAsReceiver = async (bidId) => {
  confirmingMap.value[bidId] = true
  try {
    await axios.post(`https://bidngive.onrender.com/api/bids/confirm-receive/${bidId}/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Payment confirmed')
    fetchBids()
  } catch (err) {
    toast.error(err.response?.data?.error || 'Failed to confirm')
  } finally {
    confirmingMap.value[bidId] = false
  }
}

const recommit = async (bid) => {
  try {
    await axios.post(`https://bidngive.onrender.com/api/bids/`, {
      amount: bid.amount,
      plan: bid.plan,
      type: 'investment'
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Recommit successful')
    fetchBids()
  } catch {
    toast.error('Recommit failed')
  }
}

const withdraw = async (bid) => {
  try {
    await axios.post(`https://bidngive.onrender.com/api/bids/withdraw/`, {
      amount: bid.amount
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Withdrawal successful')
    fetchBids()
  } catch {
    toast.error('Withdrawal failed')
  }
}

const whatsappLink = (number) => {
  if (!number) return '#'
  const phone = number.startsWith('0') ? '234' + number.slice(1) : number
  return `https://wa.me/${phone}`
}

const startCountdowns = () => {
  bids.value.forEach(bid => {
    if (!bid.merged_at || bid.status !== 'merged') return

    const end = new Date(bid.merged_at).getTime() + 5 * 60 * 60 * 1000

    const updateTimer = () => {
      const diff = end - Date.now()
      if (diff <= 0) {
        countdowns.value[bid.id] = '⛔ Time Expired'
      } else {
        const h = Math.floor(diff / 3600000)
        const m = Math.floor((diff % 3600000) / 60000)
        const s = Math.floor((diff % 60000) / 1000)
        countdowns.value[bid.id] = `${h}h ${m}m ${s}s`
      }
    }

    updateTimer()
    setInterval(updateTimer, 1000)
  })
}

onMounted(fetchBids)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600&display=swap');

.merge-info-page {
  padding: 40px 20px;
  background: #f3f4f6;
  min-height: 100vh;
  font-family: 'Segoe UI', sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}
.header h2 {
  font-size: 2rem;
  font-weight: 600;
  color: #111827;
}
.header p {
  color: #6b7280;
  margin-top: 6px;
  font-size: 0.95rem;
}

.bids-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.bid-card {
  background: #ffffff;
  padding: 24px;
  border-radius: 16px;
  max-width: 740px;
  margin: auto;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s ease;
}
.bid-card:hover {
  transform: translateY(-2px);
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 18px;
}
.info-row {
  display: flex;
  justify-content: space-between;
}
.label {
  color: #6b7280;
  font-weight: 500;
}
.value {
  font-weight: bold;
  color: #111827;
}
.amount {
  color: #0c69c8;
}
.status.merged {
  color: #0c69c8;
}
.status.paid {
  color: #16a34a;
}
.countdown {
  color: #b45309;
  font-weight: 600;
}

.warning {
  margin-top: 6px;
  font-size: 0.9rem;
  color: #b91c1c;
  font-weight: 500;
}

.receiver-box {
  background-color: #f9fafb;
  padding: 14px 18px;
  border-radius: 12px;
  margin-bottom: 20px;
  font-size: 0.95rem;
  border: 1px solid #e5e7eb;
}
.receiver-box h4 {
  margin-bottom: 8px;
  color: #111827;
  font-size: 1rem;
  font-weight: 600;
}
.whatsapp-link {
  color: #10b981;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
}
.wa-icon {
  width: 18px;
  height: 18px;
  opacity: 0.8;
}

.upload-section,
.confirm-section {
  margin-top: 20px;
}

input[type="file"] {
  margin-top: 8px;
  margin-bottom: 10px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 8px 12px;
  width: 100%;
  font-size: 0.95rem;
}

.preview {
  max-width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  margin-top: 12px;
}

.btn {
  background-color: #047857;
  color: white;
  padding: 10px 18px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s ease;
}
.btn:hover {
  background-color: #065f46;
}
.confirm-btn {
  background-color: #10b981;
}
.confirm-btn:hover {
  background-color: #059669;
}
.actions-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
}
.recommit-btn {
  background-color: #2563eb;
}
.recommit-btn:hover {
  background-color: #1d4ed8;
}
.withdraw-btn {
  background-color: #dc2626;
}
.withdraw-btn:hover {
  background-color: #b91c1c;
}
.success-msg {
  margin-top: 20px;
  font-weight: bold;
  color: #16a34a;
  text-align: center;
}
.loading {
  text-align: center;
  font-size: 1rem;
  color: #6b7280;
  margin-top: 60px;
}
</style>
