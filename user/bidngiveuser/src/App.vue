<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import NavBar from '@/components/NavBar.vue';
import WhatsappCard from '@/components/WhatsappCard.vue'; // ✅ your OTP modal component
import axios from 'axios';

const route = useRoute();
const router = useRouter();

const user = ref(null);
const showVerifyModal = ref(false);
const tokenIsValid = ref(false);

const hiddenRoutes = ['signup', 'otp', 'login', 'tos', '404'];
const showNav = computed(() => route.name && !hiddenRoutes.includes(route.name));

const checkAuthAndPhone = async () => {
  const token = localStorage.getItem("access_token");
  if (!token && !hiddenRoutes.includes(route.name)) {
    router.replace({ name: 'login' });
    return;
  }

  try {
    const res = await axios.get('http://127.0.0.1:8000/api/accounts/me/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    user.value = res.data;
    tokenIsValid.value = true;
    showVerifyModal.value = !res.data.is_phone_verified;
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

    <!-- WhatsApp OTP Modal -->
    <WhatsappCard
      v-if="tokenIsValid && showVerifyModal"
      :user="user"
      @verified="showVerifyModal = false"
    />

    <RouterView v-if="tokenIsValid" />
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: 'Segoe UI', sans-serif;
  background-color: #f5f5f5;
}
</style>
