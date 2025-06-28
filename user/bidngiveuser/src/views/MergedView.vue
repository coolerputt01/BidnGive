<template>
  <main class="merge-info-page">
    <section class="header">
      <h2>Merged Bids</h2>
      <p>Below are your active merges. Please take necessary action within 5 hours of merging.</p>
    </section>

    <div v-if="bids.length" class="bids-container">
      <div v-for="bid in bids" :key="bid.id" class="bid-card">
        <div class="details-grid">
          <div class="info-row">
            <span class="label">Amount to Pay</span>
            <span class="value amount">₦{{ bid.amount.toLocaleString() }}</span>
          </div>
          <div class="info-row">
            <span class="label">Expected Return</span>
            <span class="value">₦{{ bid.expected_return.toLocaleString() }}</span>
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

        <div class="receiver-box">
          <h4>Receiver Details</h4>
          <p>
            <strong>Phone:</strong>
            <a :href="`https://wa.me/234${bid.receiver_phone}`" target="_blank" class="whatsapp-link">
              {{ bid.receiver_phone }}
              <img src="/icons/whatsapp.svg" alt="WhatsApp" class="wa-icon" />
            </a>
          </p>
        </div>

        <div v-if="bid.status === 'merged'" class="upload-section">
          <label>Upload Payment Proof:</label>
          <input type="file" @change="e => handleFileChange(e, bid.id)" accept="image/*" />
          <button class="btn" @click="() => uploadProof(bid.id)" :disabled="uploadingMap[bid.id]">
            {{ uploadingMap[bid.id] ? 'Uploading...' : 'Submit Payment Proof' }}
          </button>
        </div>

        <div v-if="bid.status === 'paid' && !bid.receiver_confirmed" class="confirm-section">
          <p class="info-text">Waiting for receiver to confirm payment.</p>
          <button class="btn confirm-btn" @click="() => confirmAsReceiver(bid.id)" :disabled="confirmingMap[bid.id]">
            {{ confirmingMap[bid.id] ? 'Confirming...' : 'Confirm Payment Received' }}
          </button>
        </div>

        <div v-if="bid.status === 'paid' && bid.receiver_confirmed" class="success-msg">
          ✅ Payment has been confirmed by the receiver.
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

const bids = ref([])
const countdowns = ref({})
const token = localStorage.getItem('access_token')
const fileMap = ref({})
const uploadingMap = ref({})
const confirmingMap = ref({})

const fetchBids = async () => {
  try {
    const res = await axios.get(`https://bidngive.onrender.com/api/bids/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const mergedBids = res.data.filter(b => b.status === 'merged' || b.status === 'paid')
    bids.value = mergedBids
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
    toast.success('Proof uploaded')
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
    const res = await axios.post(`https://bidngive.onrender.com/api/bids/confirm-receive/${bidId}/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success(res.data.message)
    fetchBids()
  } catch (err) {
    toast.error(err.response?.data?.error || 'Failed to confirm')
  } finally {
    confirmingMap.value[bidId] = false
  }
}

const startCountdowns = () => {
  bids.value.forEach(bid => {
    if (!bid.merged_at) return
    const end = new Date(bid.merged_at).getTime() + 5 * 60 * 60 * 1000
    const updateTimer = () => {
      const diff = end - new Date().getTime()
      if (diff <= 0) {
        countdowns.value[bid.id] = "⛔ Time Expired"
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
.merge-info-page {
  padding: 40px 20px;
  font-family: 'Segoe UI', sans-serif;
  background: #f3f3f3;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h2 {
  font-size: 2.2em;
  color: #191919;
}

.header p {
  font-size: 1em;
  color: #555;
}

.bids-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.bid-card {
  background: #fff;
  padding: 25px;
  border-radius: 16px;
  max-width: 720px;
  margin: auto;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.95em;
}

.label {
  color: #555;
  font-weight: 500;
}

.value {
  font-weight: bold;
  color: #222;
}

.amount {
  font-size: 1.1em;
  color: #0c69c8;
}

.status.paid {
  color: #1a8917;
}

.status.pending {
  color: #d97706;
}

.status.merged {
  color: #0c69c8;
}

.countdown {
  color: #c2410c;
  font-weight: bold;
}

.receiver-box {
  background-color: #f8fafc;
  padding: 16px;
  border-radius: 10px;
  margin-bottom: 20px;
  font-size: 0.95em;
}

.receiver-box h4 {
  margin-bottom: 10px;
  color: #111827;
}

.whatsapp-link {
  color: #10b981;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
}

.wa-icon {
  width: 18px;
  height: 18px;
  vertical-align: middle;
}

.upload-section,
.confirm-section {
  margin-top: 20px;
}

input[type="file"] {
  margin-top: 8px;
  margin-bottom: 12px;
}

.btn {
  display: inline-block;
  background-color: #04724D;
  color: white;
  padding: 10px 18px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: rgb(3, 197, 133);
}

.confirm-btn {
  background-color: #10b981;
}

.confirm-btn:hover {
  background-color: #059669;
}

.success-msg {
  margin-top: 20px;
  font-weight: bold;
  color: #16a34a;
  font-size: 1em;
}

.loading {
  text-align: center;
  font-size: 1.1em;
  color: #555;
  margin-top: 50px;
}
</style>
