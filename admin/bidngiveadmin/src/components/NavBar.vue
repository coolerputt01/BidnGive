<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

const isOpen = ref(false);
const toggleMenu = () => {
  isOpen.value = !isOpen.value;
};

const route = useRoute();

// Hide navbar if on login page
const showNavbar = computed(() => {
    if(route.name === 'Login'){
      return false
    }

    return true;
});
</script>

<template>
  <nav v-if="showNavbar" class="navbar">
    <div class="logo">BID &quot;N&quot; GIVE Admin</div>

    <!-- Hamburger -->
    <button class="menu-toggle" @click="toggleMenu" aria-label="Toggle Navigation Menu">
      ☰
    </button>

    <!-- Navigation Links -->
    <ul :class="['nav-links', { open: isOpen }]">
      <li><router-link to="/dashboard" @click="isOpen = false">Dashboard</router-link></li>
      <li><router-link to="/manual-merging" @click="isOpen = false">Manual Merging</router-link></li>
      <li><router-link to="/change-logins" @click="isOpen = false">Change Logins</router-link></li>
      <li><router-link to="/create-investment" @click="isOpen = false">Create Investment</router-link></li>
      <li><router-link to="/all-bids" @click="isOpen = false">All Bids</router-link></li>
      <li><router-link to="/create-withdrawal" @click="isOpen = false">Create Withdrawal</router-link></li>
      <li><router-link to="/user-details" @click="isOpen = false">Users</router-link></li>
      <li><router-link to="/user-page" @click="isOpen = false">Users List</router-link></li>
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
  padding: 6px 10px;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}
.nav-links a:hover {
  background-color: #e0f7eb;
}
.nav-links a.router-link-exact-active {
  background-color: #e0f7eb;
  font-weight: 700;
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
