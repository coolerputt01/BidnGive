<template>
  <main class="admin-dashboard">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="title-block">
        <h1>📋 Admin Control Panel</h1>
        <p>Quick actions to manage users, investments, and settings.</p>
      </div>
    </header>

    <!-- Admin Action Grid -->
    <section class="dashboard-grid">
      <div class="dashboard-card" @click="goTo('/cancel-investment')">
        <div class="icon">🚫</div>
        <h3>Cancel Recommitment</h3>
        <p>Manually cancel recommitments for stuck bids.</p>
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

        <div class="dashboard-card" @click="goTo('/user-list')">
          <div class="icon">👥</div>
          <h3>User List</h3>
          <p>Browse and manage the list of all users.</p>
        </div>

      <div class="dashboard-card" @click="goTo('/withdrawals')">
        <div class="icon">💸</div>
        <h3>Withdrawals</h3>
        <p>Manage referral bonus withdrawal requests.</p>
      </div>

      <div class="dashboard-card" @click="goTo('/manual-merge')">
        <div class="icon">🔄</div>
        <h3>Manual Merging</h3>
        <p>Manually merge pending bids during auction windows.</p>
      </div>


      <div class="dashboard-card" @click="goTo('/change-password')">
        <div class="icon">🔐</div>
        <h3>Change User Login</h3>
        <p>Reset or update a user's login password.</p>
      </div>
    </section>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const goTo = (path) => router.push(path)
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
  background: #f5f7fa;
  min-height: 100vh;
  font-family: 'Segoe UI', sans-serif;
}

.dashboard-header {
  margin-bottom: 2rem;
  text-align: center;
}

.title-block h1 {
  font-size: 2rem;
  color: #004f28;
  margin-bottom: 0.3rem;
}

.title-block p {
  font-size: 1rem;
  color: #555;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.dashboard-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.dashboard-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
}

.icon {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #17a35e;
}

.dashboard-card h3 {
  font-size: 1.2rem;
  color: #191919;
  margin-bottom: 0.5rem;
}

.dashboard-card p {
  color: #666;
  font-size: 0.95rem;
}
</style>
