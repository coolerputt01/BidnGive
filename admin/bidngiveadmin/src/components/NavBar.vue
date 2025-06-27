<template>
  <nav class="navbar">
    <div class="logo">BID "N" GIVE Admin</div>

    <!-- Hamburger -->
    <button class="menu-toggle" @click="toggleMenu">
      ☰
    </button>

    <!-- Navigation Links -->
    <ul :class="['nav-links', { open: isOpen }]">
      <li><router-link to="/dashboard">Dashboard</router-link></li>
      <li><router-link to="/pending-bids">Pending Bids</router-link></li>
      <li><router-link to="/withdrawals">Withdrawals</router-link></li>
      <li><router-link to="/merge-settings">Merge Settings</router-link></li>
      <li><router-link to="/create-investment">Create Investment</router-link></li>
      <li><router-link to="/cancel-investment">Cancel Investment</router-link></li>
      <li><router-link to="/user-details">Users</router-link></li>
      <li><router-link to="/user-page">Users List</router-link></li>
    </ul>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const isOpen = ref(false)
const toggleMenu = () => {
  isOpen.value = !isOpen.value
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  padding: 16px 32px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', sans-serif;
  flex-wrap: wrap;
  position: relative;
}
.logo {
  font-size: 1.2em;
  font-weight: 700;
  color: #004f28;
}

/* Hamburger */
.menu-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  color: #004f28;
}

/* Links */
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

/* Responsive */
@media (max-width: 768px) {
  .menu-toggle {
    display: block;
  }

  .nav-links {
    flex-direction: column;
    width: 100%;
    display: none;
    margin-top: 12px;
  }

  .nav-links.open {
    display: flex;
  }

  .nav-links li {
    padding: 10px 0;
    border-top: 1px solid #eee;
  }

  .nav-links a {
    padding: 10px 0;
  }
}
</style>
