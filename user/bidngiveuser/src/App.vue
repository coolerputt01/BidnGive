<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import NavBar from '@/components/NavBar.vue';

const route = useRoute();
const hiddenRoutes = ['signup', 'otp', 'login', 'tos','404'];

const showNav = computed(() => {
  return route.name && !hiddenRoutes.includes(route.name);
});
</script>

<template>
  <RouterView />
  <NavBar v-if="showNav" />
</template>
