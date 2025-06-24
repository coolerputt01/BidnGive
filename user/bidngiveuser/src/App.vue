<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const hiddenRoutes = ['signup', 'otp', 'login', 'tos', '404'];

const showNav = computed(() => {
  return route.name && !hiddenRoutes.includes(route.name);
});

const tokenIsValid = ref(false);

onMounted(async () => {
  const token = localStorage.getItem("access_token");

  if (!token) {
    router.replace('/login');
    return;
  }

  try {
    // Check token by hitting a protected endpoint
    const response = await axios.get('http://127.0.0.1:8000/api/wallet/balance', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (response.status === 200) {
      tokenIsValid.value = true;
    }
  } catch (error) {
    console.error("Invalid token or not logged in:", error);
    localStorage.removeItem("access_token");
    router.replace('/login');
  }
});
</script>

<template>
  <RouterView v-if="tokenIsValid" />
  <NavBar v-if="tokenIsValid && showNav" />
</template>
