<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const otpLength = 6
const otp = ref(Array(otpLength).fill(''))
const otpRefs = ref([])
const loading = ref(false)

const phoneNumber = JSON.parse(localStorage.getItem("userInfo"))?.phone_number || ''

onMounted(() => {
  otpRefs.value = otpRefs.value.slice(0, otpLength)
})

const handleInput = (index) => {
  if (otp.value[index].length === 1 && index < otpLength - 1) {
    otpRefs.value[index + 1]?.focus()
  }
}

const handleBackspace = (index) => {
  if (otp.value[index] === '' && index > 0) {
    otpRefs.value[index - 1]?.focus()
  }
}

const handlePaste = (e) => {
  const pasted = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, otpLength)
  for (let i = 0; i < pasted.length; i++) {
    otp.value[i] = pasted[i]
  }
  otpRefs.value[Math.min(pasted.length, otpLength - 1)]?.focus()
}

const verifyOTP = async () => {
  const enteredOTP = otp.value.join('')
  if (enteredOTP.length !== otpLength) {
    toast.error("Please enter all 6 digits")
    return
  }

  loading.value = true
  try {
    const token = localStorage.getItem("access_token")
    const res = await axios.post("https://bidngive.onrender.com/api/accounts/verify-whatsapp-otp/", {
      otp: enteredOTP,
      phone: phoneNumber
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })

    toast.success(res.data.message || "Phone verified!")
    emit('verified')
    // Next step (emit event or redirect)
  } catch (err) {
    toast.error(err.response?.data?.error || "Invalid OTP")
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="otp-overlay">
    <div class="otp-card">
      <h3>Verify WhatsApp</h3>
      <p class="desc">Enter the 6-digit code sent to <b>{{ phoneNumber }}</b></p>

      <div class="otp-inputs" @paste.prevent="handlePaste">
        <input
          v-for="(digit, index) in otp"
          :key="index"
          type="text"
          maxlength="1"
          v-model="otp[index]"
          @input="handleInput(index)"
          @keydown.backspace="handleBackspace(index)"
          ref="otpRefs"
        />
      </div>

      <button class="verify-btn" @click="verifyOTP" :disabled="loading">
        <span v-if="!loading">Verify</span>
        <span v-else class="loader"></span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.otp-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  background: rgba(245, 245, 245, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  z-index: 999;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-y: hidden;
}

.otp-card {
  width: 90%;
  max-width: 400px;
  background: white;
  border-radius: 16px;
  padding: 2rem 1.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.otp-card h3 {
  font-size: 1.4rem;
  margin-bottom: 0.3rem;
  color: #222;
}

.desc {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 1.4rem;
}

.otp-inputs {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 1.4rem;
}

.otp-inputs input {
  width: 44px;
  height: 54px;
  font-size: 1.5rem;
  text-align: center;
  border: 2px solid #ccc;
  border-radius: 10px;
  transition: border-color 0.2s;
}

.otp-inputs input:focus {
  border-color: #04724D;
  outline: none;
}

.verify-btn {
  width: 100%;
  height: 45px;
  border: none;
  background-color: #04724D;
  color: white;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.verify-btn:hover {
  opacity: 0.9;
}

.loader {
  border: 3px solid #ccc;
  border-top: 3px solid #fff;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
