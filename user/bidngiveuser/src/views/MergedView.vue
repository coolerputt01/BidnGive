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

        <div class="receiver-box">
          <h4>{{ bid.role === 'buyer' ? 'Pay To' : 'From' }} Details</h4>
          <p>
            <strong>Phone:</strong>
            <a :href="whatsappLink(bid.counterparty_phone)" target="_blank" class="whatsapp-link">
              {{ bid.counterparty_phone }}
              <img src="/icons/whatsapp.svg" alt="WhatsApp" class="wa-icon" />
            </a>
          </p>
        </div>

        <!-- BUYER UI -->
        <div v-if="bid.role === 'buyer' && bid.status === 'merged'" class="upload-section">
          <label>Upload Payment Proof:</label>
          <input type="file" @change="e => handleFileChange(e, bid.id)" accept="image/*" />
          <div v-if="fileMap[bid.id]">
            <img :src="URL.createObjectURL(fileMap[bid.id])" class="preview" />
          </div>
          <button class="btn" @click="() => uploadProof(bid.id)" :disabled="uploadingMap[bid.id]">
            {{ uploadingMap[bid.id] ? 'Uploading...' : 'Submit Payment Proof' }}
          </button>
        </div>

        <!-- SELLER UI -->
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

        <!-- Success Msg for Buyer -->
        <div v-if="bid.role === 'buyer' && bid.status === 'paid' && bid.receiver_confirmed" class="success-msg">
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

const token = localStorage.getItem('access_token')
const bids = ref([])
const countdowns = ref({})
const fileMap = ref({})
const uploadingMap = ref({})
const confirmingMap = ref({})

const fetchBids = async () => {
  try {
    const res = await axios.get(`https://bidngive.onrender.com/api/bids/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    bids.value = res.data.filter(b => b.status === 'merged' || b.status === 'paid')
    startCountdowns()
  } catch {
    toast.error('Failed to load bids')
  }
}

const whatsappLink = (number) => {
  if (!number) return '#'
  const phone = number.startsWith('0') ? '234' + number.slice(1) : number
  return `https://wa.me/${phone}`
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
    const res = await axios.post(`https://bidngive.onrender.com/api/bids/confirm-receive/${bidId}/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success(res.data.message || 'Payment confirmed')
    fetchBids()
  } catch (err) {
    toast.error(err.response?.data?.error || 'Failed to confirm payment')
  } finally {
    confirmingMap.value[bidId] = false
  }
}

const startCountdowns = () => {
  bids.value.forEach(bid => {
    if (!bid.merged_at) return
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
.merge-info-page {
  padding: 40px 20px;
  background: #f3f3f3;
  min-height: 100vh;
  font-family: 'Segoe UI', sans-serif;
}
.header {
  text-align: center;
  margin-bottom: 30px;
}
.header h2 {
  font-size: 2em;
  color: #191919;
}
.header p {
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
  color: #0c69c8;
}
.status.paid {
  color: #1a8917;
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
.whatsapp-link {
  color: #10b981;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.wa-icon {
  width: 18px;
  height: 18px;
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
  background-color: #04724D;
  color: white;
  padding: 10px 18px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}
.btn:hover {
  background-color: #03966e;
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
}
.warning {
  margin-top: 10px;
  color: #b91c1c;
  font-weight: 500;
}
.preview {
  max-width: 100%;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-top: 10px;
}
.loading {
  text-align: center;
  font-size: 1.1em;
  color: #777;
  margin-top: 50px;
}
</style>
