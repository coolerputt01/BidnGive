<template>
  <section class="create-bid-page" style="margin-bottom: 5em;">
    <!-- Header -->
    <h2 class="page-title">Investment Bid</h2>

    <!-- Auction Countdown -->
    <div class="auction-info">
      <span class="countdown">
        ⏰ Next auction starts in 
        {{ formatTime(auctionInfo.remaining_seconds) }}
      </span>
      <span
        class="status"
        :class="{ open: auctionInfo.market_status === 'open', closed: auctionInfo.market_status !== 'open' }"
      >
        {{ auctionInfo.market_status === 'open' ? 'Market Open' : 'Market Closed' }}
      </span>
    </div>

    <!-- Bid Cards -->
    <div v-if="bids.length > 0">
      <BidCard
        v-for="bid in bids"
        :key="bid.id"
        :bid="bid"
        @action="handleBidAction"
      />
    </div>

    <!-- No Bids Message -->
    <div v-else class="no-bids">
      <p>No bids available. Create one below.</p>
    </div>

    <!-- Bid Information Section -->
    <section class="bid-info">
      <h3>📘 Bid Details</h3>
      <ul>
        <li><strong>Return Rate:</strong> 50% profit on your investment</li>
        <li><strong>Duration:</strong> 24 hours before your return is processed</li>
        <li><strong>Recommitment:</strong> 100% mandatory recommitment after each completed bid</li>
        <li><strong>Payment System:</strong> Peer-to-peer (you will pay and be paid by other users directly)</li>
      </ul>
    </section>

    <!-- Create Bid Form -->
    <form class="create-form" @submit.prevent="submitBid">
      <label for="amount">Amount (₦):</label>
      <input type="number" id="amount" v-model="form.amount" required />

      <button
        type="submit"
        :disabled="bids.length > 0 && bids[0].status !== 'paid'"
      >
        {{
          bids.length > 0 && bids[0].status !== 'paid'
            ? 'Pending Bid Exists'
            : 'Create Bid'
        }}
      </button>
    </form>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { toast } from 'vue3-toastify';
import axios from 'axios';
import BidCard from '@/components/BidCard.vue';

const form = ref({ amount: '' })
const bids = ref([])
const auctionInfo = ref({ remaining_seconds: 0, market_status: '' })
const loadingSubmit = ref(false)

const fetchBids = async () => {
  const token = localStorage.getItem('access_token')
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/bids/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    bids.value = res.data;
  } catch (err) {
    console.error('Failed to fetch bids:', err)
  }
}

const fetchAuctionStatus = async () => {
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/admin/auction/status/')
    auctionInfo.value = res.data
  } catch (err) {
    console.error('Failed to fetch auction status:', err)
  }
}

const submitBid = async () => {
  if (loadingSubmit.value) return;
  loadingSubmit.value = true;
  const token = localStorage.getItem('access_token')
  if (bids.value.length > 0 && bids.value[0].status !== 'paid') {
    toast.warning('You already have a pending bid. Please wait or complete it.')
    return
  }
  const payload = {
    amount: form.value.amount,
    plan: '50_24'
  }

  try {
    await axios.post('https://bidngive.onrender.com/api/bids/', payload, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    toast.success('Bid successfully created!')
    form.value.amount = ''
    fetchBids()
    loadingSubmit.value = false;
  } catch (err) {
    console.error('Bid creation failed:', err)
    toast.error('Failed to create bid.')
  }
}

const formatTime = (seconds) => {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = seconds % 60
  return `${h}h : ${m}m : ${s}s`
}

onMounted(() => {
  fetchBids()
  fetchAuctionStatus()
})

setInterval(() => {
  if (auctionInfo.value.remaining_seconds > 0) {
    auctionInfo.value.remaining_seconds--
  }
}, 1000)

setInterval(fetchAuctionStatus, 60000)

const handleBidAction = async (bid) => {
  const token = localStorage.getItem('access_token')

  if (bid.status === 'paid') {
    try {
      await axios.post(
        'https://bidngive.onrender.com/api/bids/',
        {
          amount: bid.amount,
          plan: bid.plan,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      )

      toast.success('✅ Recommit successful! A new bid has been created.', {
        timeout: 4000,
      })

      fetchBids()
    } catch (err) {
      console.error('Recommit failed:', err)
      toast.error('❌ Failed to recommit. Please try again.')
    }
  }
}
</script>

<style scoped>
.create-bid-page {
  background-color: #f4f4f4;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.page-title {
  text-align: center;
  font-size: 1.5em;
  font-weight: bold;
  margin-bottom: 10px;
}

.auction-info {
  text-align: center;
  margin-bottom: 20px;
}

.countdown {
  display: block;
  color: #004f28;
  background-color: #e0ffe0;
  font-size: 0.9em;
  padding: 6px 12px;
  font-weight: 600;
  border-radius: 6px;
  margin-bottom: 8px;
}

.status {
  font-size: 0.9em;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 50px;
  color: #fff;
  display: inline-block;
}

.status.open {
  background-color: #17a35e;
}

.status.closed {
  background-color: #95190c;
}

.bid-info {
  background-color: #fff;
  padding: 16px 20px;
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.bid-info h3 {
  margin-bottom: 10px;
  font-size: 1.1em;
  font-weight: 700;
  color: #17a35e;
}

.bid-info ul {
  list-style: none;
  padding-left: 0;
  line-height: 1.6;
}

.bid-info li {
  margin-bottom: 6px;
  color: #444;
}

.bid-card {
  background-color: #fff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  text-align: center;
  margin-bottom: 20px;
}

.bid-amount {
  font-size: 1.1em;
  font-weight: bold;
  margin-bottom: 12px;
}

.bid-btn {
  padding: 10px 20px;
  background-color: #17a35e;
  color: white;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
}

.no-bids {
  text-align: center;
  color: #777;
  margin-bottom: 20px;
}

.create-form {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.create-form label {
  font-weight: 600;
  color: #333;
}

.create-form input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-top: 5px;
}

.create-form button {
  padding: 10px;
  background-color: #17a35e;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.create-form button:hover:enabled {
  background-color: #128f4a;
}

.create-form button:disabled {
  background-color: #ccc;
  color: #666;
  cursor: not-allowed;
}
</style>
