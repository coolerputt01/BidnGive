<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { toast } from 'vue3-toastify';
import axios from 'axios';

const router = useRouter();
const otpLength = 4;
const otp = ref(Array(4).fill(''));
const otpRefs = ref([]);
const loading = ref(false);

// Get user email from localStorage
const email = JSON.parse(localStorage.getItem("userInfo"))?.email || '';

onMounted(() => {
  otpRefs.value = otpRefs.value.slice(0, otpLength);
});

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
    const response = await axios.post("https://bidngive.onrender.com/api/accounts/verify-email/", {
      email,
      otp: enteredOTP
    });

    toast.success("Email verified! Redirecting...");
    setTimeout(() => {
      router.push('/');
    }, 1500);
  } catch (err) {
    if (err.response?.data?.error) {
      toast.error(err.response.data.error);
    } else {
      toast.error("An unexpected error occurred");
    }
  } finally {
    loading.value = false;
  }
};
</script>

<template>
    <main style="background-color: #EBEBD3;width: 100vw;height: 100vh;">
        <section style="display: flex;justify-content: center;align-items: center;width: 100%;height: 100%;">
            <div style="padding: 30px;border-radius: 6%;background-color: #fff;">
                <div style="line-height: 23px;">
                    <h1 style="font-size: 1.7em;font-weight: 650;">Verify OTP</h1>
                    <div style="font-weight: 450;font-size: 0.9em;line-height: 6px;color: grey;">
                        <p>We sent an OTP to <b style="color: #000">{{ email }}</b></p>
                        <span>Enter it below to continue.</span>
                    </div>
                </div>
                <div style="margin-top: 10%; display: flex; justify-content: center; align-items: center; gap: 3%;">
                    <div v-for="(digit, index) in otp" :key="index">
                        <input
                            style="outline: none;border: 1px solid grey;padding: 3px;border-radius: 9px;width: 3em;height: 3em;font-size: 1.2em;text-align: center;"
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
                <div style="width: 100%;margin-top: 12%;">
                    <span style="color: grey;text-align: left;font-size: 0.8em;display: flex;justify-content: flex-start;align-items: center;gap: 3%;">Resend available: <a href="#" style="font-weight: 600;cursor: pointer;text-decoration: none;">Resend OTP</a></span>
                </div>
                <div style="margin-top: 8%;">
                    <button @click.prevent="verifyOTP" :disabled="loading" style="width: 100%;height: 3em;color: #fff;outline: none;border: none;background-color: #04724D;cursor: pointer;text-align: center;display: flex;justify-content: center;align-items: center;">
                        <span v-if="!loading">Verify</span>
                        <div v-else class="loader"></div>
                    </button>
                </div>
                <div>
                    <p style="color: grey;font-size: 0.8em;text-align: center;cursor: pointer;" @click="router.go(-1)">← Back to Login</p>
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
  border-top: 3px solid #fff; /* Blue */
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 2s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>