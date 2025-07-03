<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';

const route = useRoute();
const router = useRouter();

const user = ref(null);
const tokenIsValid = ref(false);

const hiddenRoutes = ['signup', 'otp', 'login', 'tos', '404','banned'];
const showNav = computed(() => route.name && !hiddenRoutes.includes(route.name));

const checkAuthAndPhone = async () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
  if (!route.name || !hiddenRoutes.includes(route.name)) {
    router.replace({ name: 'login' });
    return;
  }
}

  try {
    const res = await axios.get('https://bidngive.onrender.com/api/accounts/me/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    user.value = res.data;
    tokenIsValid.value = true;
  } catch (err) {
    console.error('Auth check failed:', err);
    localStorage.removeItem("access_token");
    router.replace({ name: 'login' });
  }
};


onMounted(checkAuthAndPhone);
</script>

<template>
  <div>
    <NavBar v-if="tokenIsValid && showNav" />
    <RouterView v-if="tokenIsValid || ['login', 'signup', 'otp'].includes(route.name)"  />
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: 'Segoe UI', sans-serif;
  background-color: #f5f5f5;
}
</style>
