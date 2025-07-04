<template>
  <main class="admin-dashboard">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="title-block">
        <h1>📋 Admin Control Panel</h1>
        <p>Quick actions to manage users, investments, and settings.</p>
      </div>
    </header>

    <!-- Auction Status -->
    <section class="auction-status">
      <div class="status-card">
        <h3>🕒 Auction Status</h3>
        <p><strong>Market:</strong> {{ marketStatus || 'Loading...' }}</p>
        <p><strong>Next Auction:</strong> {{ nextAuctionTime || '---' }}</p>
        <p><strong>Countdown:</strong> {{ formattedCountdown }}</p>
      </div>
    </section>

    <!-- Admin Cards -->
    <section class="dashboard-grid">
      <div class="dashboard-card" @click="goTo('/all-bids')">
        <div class="icon">📄</div>
        <h3>All Bids</h3>
        <p>View and manage all investment bids across the platform.</p>
      </div>


      <div class="dashboard-card" @click="goTo('/create-investment')">
        <div class="icon">➕</div>
        <h3>Create Investment</h3>
        <p>Create a new investment on behalf of any user.</p>
      </div>

      <div class="dashboard-card" @click="goTo('/user-details')">
        <div class="icon">👤</div>
        <h3>User Details</h3>
        <p>View individual user profiles and details.</p>
      </div>

      <div class="dashboard-card" @click="goTo('/user-page')">
        <div class="icon">👥</div>
        <h3>User List</h3>
        <p>Browse and manage the list of all users.</p>
      </div>

      <div class="dashboard-card" @click="goTo('/manual-merging')">
        <div class="icon">🔄</div>
        <h3>Manual Merging</h3>
        <p>Manually merge pending bids during auction windows.</p>
      </div>

      <div class="dashboard-card" @click="goTo('/change-logins')">
        <div class="icon">🔐</div>
        <h3>Change User Login</h3>
        <p>Reset or update a user's login password.</p>
      </div>

      <!-- Add this inside the <section class="dashboard-grid"> with the other cards -->
      <div class="dashboard-card" @click="goTo('/create-withdrawal')">
        <div class="icon">📤</div>
        <h3>Create Withdrawal</h3>
        <p>Submit a withdrawal bid for a user (waits for auction).</p>
      </div>

    </section>
  </main>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const goTo = (path) => router.push(path)

const marketStatus = ref('')
const nextAuctionTime = ref('')
const countdown = ref(0)
let interval = null

const formattedCountdown = computed(() => {
  const total = countdown.value
  const hrs = String(Math.floor(total / 3600)).padStart(2, '0')
  const mins = String(Math.floor((total % 3600) / 60)).padStart(2, '0')
  const secs = String(total % 60).padStart(2, '0')
  return `${hrs}:${mins}:${secs}`
})

const fetchAuctionData = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const res = await axios.get('https://bidngive.onrender.com/api/admin/auction/status/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    marketStatus.value = res.data.market_status
    nextAuctionTime.value = res.data.next_auction
    countdown.value = res.data.remaining_seconds || 0

    if (interval) clearInterval(interval)
    startCountdown()
  } catch (err) {
    console.error('Failed to fetch auction status', err)
  }
}

const startCountdown = () => {
  interval = setInterval(() => {
    if (countdown.value > 0) {
      countdown.value--
    } else {
      clearInterval(interval)
    }
  }, 1000)
}

onMounted(fetchAuctionData)
onBeforeUnmount(() => clearInterval(interval))
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
  background: #f5f7fa;
  min-height: 100vh;
  font-family: 'Segoe UI', sans-serif;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 2rem;
}
.title-block h1 {
  font-size: 2rem;
  color: #004f28;
}
.title-block p {
  font-size: 1rem;
  color: #555;
}

.auction-status {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}
.status-card {
  background: #e6ffed;
  padding: 1.2rem 2rem;
  border-radius: 12px;
  border-left: 5px solid #1e8449;
  max-width: 420px;
  width: 100%;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}
.status-card h3 {
  color: #1e8449;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.status-card p {
  color: #222;
  font-size: 0.95rem;
  margin: 6px 0;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.dashboard-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  transition: 0.2s ease;
  cursor: pointer;
}
.dashboard-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
}
.icon {
  font-size: 2rem;
  color: #17a35e;
  margin-bottom: 1rem;
}
.dashboard-card h3 {
  font-size: 1.2rem;
  color: #191919;
  margin-bottom: 0.4rem;
}
.dashboard-card p {
  font-size: 0.95rem;
  color: #666;
}
</style>
