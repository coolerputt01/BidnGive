<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const navItems = [
  { label: 'Home', path: '/dashboard', icon: 'home' },
  { label: 'Bids', path: '/bid', icon: 'bid' },
  { label: 'Withdrawals', path: '/withdraw', icon: 'withdraw', noFilled: true },
  { label: 'Merge', path: '/merge-info', icon: 'auction',noFilled: true },
  { label: 'Profile', path: '/profile', icon: 'profile' }
]

const isActive = (path) => route.path === path
</script>

<template>
  <section class="bottom-nav">
    <nav class="nav-bar">
      <a
        v-for="item in navItems"
        :key="item.path"
        @click.prevent="router.push(item.path)"
        class="nav-link"
        :class="{ active: isActive(item.path) }"
      >
        <img
          :src="`/icons/${item.icon}${isActive(item.path) && !item.noFilled ? '-filled' : ''}.svg`"
          :alt="item.label"
          class="nav-icon"
        />
        <span>{{ item.label }}</span>
      </a>
    </nav>
  </section>
</template>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  width: 100vw;
  z-index: 1000;
  background-color: #fff;
  box-shadow: 0 -1px 6px rgba(0, 0, 0, 0.05);
  border-top: 1px solid #eee;
}

.nav-bar {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  padding: 10px 0;
  font-family: 'Inter', sans-serif;
  font-size: 0.8em;
}

.nav-link {
  text-decoration: none;
  color: #444;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: #17a35e;
}

.nav-link.active {
  color: #17a35e;
  font-weight: 600;
}

.nav-icon {
  width: 1.1em;
  height: 1.1em;
  transition: transform 0.2s ease;
}

.nav-link.active .nav-icon {
  transform: scale(1.1);
}
</style>
