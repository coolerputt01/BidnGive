<template>
  <nav class="navbar">
    <div class="logo">BID "N" GIVE Admin</div>
    <ul class="nav-links">
      <li><router-link to="/admin/dashboard">Dashboard</router-link></li>
      <li><router-link to="/admin/pending-bids">Pending Bids</router-link></li>
      <li><router-link to="/admin/withdrawals">Withdrawals</router-link></li>
      <li><router-link to="/admin/merge-settings">Merge Settings</router-link></li>
      <li><router-link to="/admin/create-investment">Create Investment</router-link></li>
      <li><router-link to="/admin/cancel-investment">Cancel Investment</router-link></li>
      <li><router-link to="/admin/user-management">Users</router-link></li>
    </ul>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  padding: 16px 32px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', sans-serif;
}
.logo {
  font-size: 1.2em;
  font-weight: 700;
  color: #004f28;
}
.nav-links {
  list-style: none;
  display: flex;
  gap: 20px;
}
.nav-links a {
  text-decoration: none;
  color: #004f28;
  font-weight: 600;
}
.nav-links a.router-link-exact-active {
  border-bottom: 2px solid #004f28;
}
</style>
