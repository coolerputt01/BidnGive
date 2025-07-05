<template>
  <section class="bids-page" style="padding-bottom: 7em;">
    <!-- Header -->
    <div class="page-header">
      <h1>Your Investment Bids</h1>
      <p>Track and manage your investment and withdrawal bids below.</p>
    </div>

    <!-- Filter Tabs -->
    <div class="filter-tabs">
      <button
        v-for="option in filterOptions"
        :key="option"
        :class="{ active: filter === option }"
        @click="filter = option"
      >
        {{ option }}
      </button>
    </div>

    <!-- Auction Info -->
    <div class="auction-info">
      <span class="countdown">
        ⏰ Auction in {{ formatTime(auctionInfo.remaining_seconds) }}
      </span>
      <span class="status" :class="auctionInfo.market_status">
        {{ auctionInfo.market_status === 'open' ? 'Market Open' : 'Market Closed' }}
      </span>
    </div>

    <!-- Bid List -->
    <div class="bid-list" v-if="filteredBids.length">
      <div class="bid-card" v-for="bid in filteredBids" :key="bid.id">
        <BidCard v-if="bid.type === 'investment'" :bid="bid" @action="fetchBids" />
        <SellerBidCard v-else-if="bid.type === 'withdrawal'" :bid="bid" @action="fetchBids" />
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="no-bids">
      <img src="/icons/empty.svg" alt="No Bids" class="empty-img" />
      <p>No {{ filter.toLowerCase() }} bids available.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import axios from 'axios'
import BidCard from '@/components/BidCard.vue'
import SellerBidCard from '@/components/SellerBidCard.vue'

const bids = ref([])
const auctionInfo = ref({ remaining_seconds: 0, market_status: '' })
const interval = ref(null)
const token = localStorage.getItem('access_token')

const filter = ref('All')
const filterOptions = ['All', 'Pending', 'Active', 'Completed']

const fetchBids = async () => {
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/bids/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    bids.value = res.data.filter(b => b.type === 'investment' || b.type === 'withdrawal')
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

const filteredBids = computed(() => {
  if (filter.value === 'All') return bids.value
  if (filter.value === 'Pending') return bids.value.filter(b => b.status === 'pending')
  if (filter.value === 'Active') return bids.value.filter(b => b.status === 'merged')
  if (filter.value === 'Completed') return bids.value.filter(b => b.status === 'paid')
  return bids.value
})

const formatTime = (seconds) => {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = seconds % 60
  return `${h}h ${m}m ${s}s`
}

onMounted(() => {
  fetchBids()
  fetchAuctionStatus()
  interval.value = setInterval(() => {
    if (auctionInfo.value.remaining_seconds > 0) {
      auctionInfo.value.remaining_seconds--
    }
  }, 1000)
})

onBeforeUnmount(() => {
  if (interval.value) clearInterval(interval.value)
})
</script>

<style scoped>
.bids-page {
  padding: 2rem;
  background-color: #f5f7fb;
  min-height: 100vh;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}
.page-header h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #191919;
}
.page-header p {
  font-size: 1rem;
  color: #555;
}

.filter-tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}
.filter-tabs button {
  padding: 0.6rem 1.4rem;
  border: none;
  border-radius: 30px;
  background-color: #eee;
  color: #333;
  font-weight: 600;
  transition: 0.3s;
  cursor: pointer;
}
.filter-tabs button.active {
  background-color: #17a35e;
  color: #fff;
}

.auction-info {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}
.countdown {
  background-color: #e0ffe0;
  padding: 0.5rem 1.2rem;
  border-radius: 20px;
  font-weight: 600;
  color: #004f28;
}
.status {
  padding: 0.5rem 1.2rem;
  border-radius: 20px;
  font-weight: 600;
  color: #fff;
  text-transform: capitalize;
}
.status.open {
  background-color: #17a35e;
}
.status.closed {
  background-color: #95190c;
}

.bid-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.bid-card {
  background-color: #fff;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.no-bids {
  text-align: center;
  color: #888;
  margin-top: 4rem;
}
.empty-img {
  width: 120px;
  margin-bottom: 1rem;
}
</style>
