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
      <div class="dashboard-card" @click="goTo('/admin/cancel-recommitment')">
        <div class="icon">🚫</div>
        <h3>Cancel Recommitment</h3>
        <p>Manually cancel recommitments for stuck bids.</p>
      </div>

      <div class="dashboard-card" @click="goTo('/admin/create-investment')">
        <div class="icon">➕</div>
        <h3>Create Investment</h3>
        <p>Create a new investment on behalf of any user.</p>
      </div>

      <div class="dashboard-card" @click="goTo('/admin/user-management')">
        <div class="icon">👥</div>
        <h3>Users & List</h3>
        <p>View users, suspend accounts, or inspect referrals.</p>
      </div>

      <div class="dashboard-card" @click="goTo('/admin/withdrawals')">
        <div class="icon">💸</div>
        <h3>Withdrawals</h3>
        <p>Manage referral bonus withdrawal requests.</p>
      </div>

      <div class="dashboard-card" @click="goTo('/admin/pending-bids')">
        <div class="icon">🕒</div>
        <h3>Pending Bids</h3>
        <p>Review bids awaiting merge or action.</p>
      </div>
    </section>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goTo = (path) => {
  router.push(path);
};
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
