<template>
  <main class="dashboard">
    <header class="dashboard-header">
      <h2>Admin Dashboard</h2>
    </header>

    <section class="button-panel">
      <button class="admin-btn" @click="goTo('/admin/pending-bids')">
        🕒 Pending Bids
      </button>
      <button class="admin-btn" @click="goTo('/admin/manual-merge')">
        🔀 Manual Merge
      </button>
      <button class="admin-btn" @click="goTo('/admin/withdrawals')">
        💸 Withdrawals
      </button>
      <button class="admin-btn" @click="goTo('/admin/merge-settings')">
        ⏰ Merge Time Settings
      </button>
      <button class="admin-btn" @click="goTo('/admin/manage-investments')">
        📈 Manage Investments
      </button>
      <button class="admin-btn" @click="goTo('/admin/user-management')">
        👥 Manage Users
      </button>
    </section>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.clear()
  router.push('/admin-login')
}

const goTo = (path) => {
  router.push(path)
}
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
  margin-bottom: 2.5rem;
}

.dashboard-header h2 {
  font-size: 1.8rem;
  color: #191919;
}

.logout-btn {
  background-color: #95190C;
  color: #fff;
  padding: 0.6rem 1.4rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}
.logout-btn:hover {
  background-color: #b92c1f;
}

.button-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 400px;
  margin: auto;
}

.admin-btn {
  padding: 1rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  background-color: #004f28;
  color: white;
  text-align: left;
  transition: background-color 0.25s ease;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.admin-btn:hover {
  background-color: #007a44;
}
</style>
