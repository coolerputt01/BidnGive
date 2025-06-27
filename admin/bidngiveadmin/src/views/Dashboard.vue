<template>
  <main class="dashboard">
    <header class="dashboard-header">
      <h2>Admin Dashboard</h2>
      <button class="logout-btn" @click="logout">Logout</button>
    </header>

    <section class="cards">
      <div class="card" @click="goTo('/admin/pending-bids')">
        <h3>Pending Bids</h3>
        <p>View and manage auction-room bids</p>
      </div>
      <div class="card" @click="goTo('/admin/manual-merge')">
        <h3>Manual Merge</h3>
        <p>Trigger a merge for available bids</p>
      </div>
      <div class="card" @click="goTo('/admin/withdrawals')">
        <h3>Withdrawals</h3>
        <p>View and mark withdrawal requests</p>
      </div>
      <div class="card" @click="goTo('/admin/merge-settings')">
        <h3>Merge Time Settings</h3>
        <p>Update morning and evening auction time</p>
      </div>
      <div class="card" @click="goTo('/admin/manage-investments')">
        <h3>Manage Investments</h3>
        <p>Create or cancel user bids</p>
      </div>
    </section>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const logout = () => {
  localStorage.clear();
  router.push('/admin-login');
};

const goTo = (path) => {
  router.push(path);
};
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  background-color: #fff;
  min-height: 100vh;
  font-family: 'Segoe UI', sans-serif;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-header h2 {
  font-size: 1.8rem;
  color: #191919;
}

.logout-btn {
  background-color: #95190C;
  color: #fff;
  padding: 0.5rem 1.2rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.card {
  background-color: #ebebd3;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-4px);
  background-color: #e0ffe0;
}

.card h3 {
  margin-bottom: 0.5rem;
  color: #004f28;
  font-size: 1.2rem;
}

.card p {
  color: #444;
  font-size: 0.95rem;
}
</style>
