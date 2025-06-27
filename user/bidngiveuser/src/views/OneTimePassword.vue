<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { toast } from 'vue3-toastify';
import axios from 'axios';

const router = useRouter();
const otpLength = 4;
const otp = ref(Array(otpLength).fill(''));
const otpRefs = ref([]);
const loading = ref(false);

// Email from localStorage
const email = JSON.parse(localStorage.getItem("userInfo"))?.email || '';

// Countdown timer state
const resendTimer = ref(300); // 5 minutes in seconds
let timerInterval = null;

const formattedTimer = computed(() => {
  const minutes = Math.floor(resendTimer.value / 60);
  const seconds = resendTimer.value % 60;
  return `${minutes}m ${seconds < 10 ? '0' : ''}${seconds}s`;
});

const startResendCountdown = () => {
  clearInterval(timerInterval);
  resendTimer.value = 300;
  timerInterval = setInterval(() => {
    if (resendTimer.value > 0) {
      resendTimer.value--;
    } else {
      clearInterval(timerInterval);
    }
  }, 1000);
};

const handleInput = (index) => {
  if (otp.value[index].length === 1 && index < otpLength - 1) {
    otpRefs.value[index + 1]?.focus();
  }
};

const handleBackspace = (index) => {
  if (otp.value[index] === '' && index > 0) {
    otpRefs.value[index - 1]?.focus();
  }
};

const verifyOTP = async () => {
  const enteredOTP = otp.value.join('');
  if (enteredOTP.length !== otpLength) {
    toast.error("Please enter the full OTP");
    return;
  }

  loading.value = true;

  try {
    await axios.post("https://bidngive.onrender.com/api/accounts/verify-email/", {
      email,
      otp: enteredOTP
    });

    toast.success("Email verified! Redirecting...");
    setTimeout(() => {
      router.push('/');
    }, 1500);
  } catch (err) {
    toast.error(err.response?.data?.error || "An unexpected error occurred");
  } finally {
    loading.value = false;
  }
};

const resendOTP = async () => {
  if (resendTimer.value > 0) return;

  try {
    await axios.post("https://bidngive.onrender.com/api/accounts/resend-email-otp/", { email });
    toast.success("OTP resent to your email.");
    startResendCountdown();
  } catch (err) {
    toast.error("Failed to resend OTP");
  }
};

onMounted(() => {
  otpRefs.value = otpRefs.value.slice(0, otpLength);
  startResendCountdown();
});

onUnmounted(() => {
  clearInterval(timerInterval);
});
</script>

<template>
  <main style="background-color: #EBEBD3; width: 100vw; height: 100vh;">
    <section style="display: flex; justify-content: center; align-items: center; width: 100%; height: 100%;">
      <div style="padding: 30px; border-radius: 6%; background-color: #fff;">
        <div style="line-height: 23px;">
          <h1 style="font-size: 1.7em; font-weight: 650;">Verify OTP</h1>
          <div style="font-weight: 450; font-size: 0.9em; line-height: 6px; color: grey;">
            <p>We sent an OTP to <b style="color: #000">{{ email }}</b></p>
            <span>Enter it below to continue.</span>
          </div>
        </div>

        <div style="margin-top: 10%; display: flex; justify-content: center; align-items: center; gap: 3%;">
          <div v-for="(digit, index) in otp" :key="index">
            <input
              style="outline: none; border: 1px solid grey; padding: 3px; border-radius: 9px; width: 3em; height: 3em; font-size: 1.2em; text-align: center;"
              v-model="otp[index]"
              @input="handleInput(index)"
              @keydown.backspace="handleBackspace(index)"
              maxlength="1"
              class="otp-input"
              ref="otpRefs"
              type="text"
            />
          </div>
        </div>

        <div style="width: 100%; margin-top: 12%;">
          <span style="color: grey; font-size: 0.8em; display: flex; justify-content: flex-start; gap: 3%;">
            <template v-if="resendTimer > 0">
              Resend available in: <b>{{ formattedTimer }}</b>
            </template>
            <template v-else>
              <a href="#" @click.prevent="resendOTP" style="font-weight: 600; text-decoration: none; cursor: pointer;">Resend OTP</a>
            </template>
          </span>
        </div>

        <div style="margin-top: 8%;">
          <button @click.prevent="verifyOTP" :disabled="loading" style="width: 100%; height: 3em; color: #fff; outline: none; border: none; background-color: #04724D; cursor: pointer; text-align: center; display: flex; justify-content: center; align-items: center;">
            <span v-if="!loading">Verify</span>
            <div v-else class="loader"></div>
          </button>
        </div>

        <div>
          <p style="color: grey; font-size: 0.8em; text-align: center; cursor: pointer;" @click="router.go(-1)">← Back to Login</p>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type=number] {
  -moz-appearance: textfield;
  appearance: textfield;
}
button:hover {
  transition: all 0.3s;
  opacity: 0.8;
}
.loader {
  border: 3px solid rgb(172, 172, 172); /* Light grey */
  border-top: 3px solid #fff; /* White */
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
