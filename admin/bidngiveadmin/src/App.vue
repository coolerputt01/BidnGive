<template>
  <div>
    <NavBar v-if="showNav" />
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import NavBar from '@/components/NavBar.vue';

const route = useRoute();

// Show navbar only when not on login or signup routes
const showNav = computed(() => !['/admin/login', '/admin/signup'].includes(route.path));
</script>

<style scoped>
body {
  margin: 0;
  font-family: 'Segoe UI', sans-serif;
  background-color: #f9f9f9;
}
</style>
