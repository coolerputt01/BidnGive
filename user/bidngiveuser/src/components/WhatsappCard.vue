<script setup>
import { ref, nextTick, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const props = defineProps({ user: Object })
const emit = defineEmits(['verified'])

const otpValues = ref(['', '', '', '', '', ''])
const inputRefs = Array.from({ length: 6 }, () => ref(null))
const loading = ref(false)

onMounted(() => {
  nextTick(() => inputRefs[0].value?.focus())
})

const handleInput = (e, index) => {
  const value = e.target.value.replace(/\D/g, '')
  if (value) {
    otpValues.value[index] = value[0]
    if (index < 5) {
      nextTick(() => inputRefs[index + 1].value?.focus())
    }
  } else {
    otpValues.value[index] = ''
  }
}

const handleKeydown = (e, index) => {
  if (e.key === 'Backspace' && !otpValues.value[index] && index > 0) {
    nextTick(() => inputRefs[index - 1].value?.focus())
  }
}

const handlePaste = (e) => {
  const pasted = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6)
  for (let i = 0; i < pasted.length; i++) {
    otpValues.value[i] = pasted[i]
  }
  nextTick(() => {
    if (pasted.length < 6) inputRefs[pasted.length]?.value?.focus()
  })
}

const verifyOTP = async () => {
  const otp = otpValues.value.join('')
  if (otp.length !== 6) {
    toast.error("Enter all 6 digits")
    return
  }

  try {
    loading.value = true
    const token = localStorage.getItem("access_token")
    const res = await axios.post("http://127.0.0.1:8000/api/accounts/verify-whatsapp-otp/", { otp }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success(res.data.message)
    emit('verified')
  } catch (err) {
    toast.error(err.response?.data?.error || "Invalid OTP")
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="overlay">
    <div class="modal">
      <h2>Verify WhatsApp</h2>
      <p>Enter the 6-digit OTP sent to your WhatsApp number</p>

      <div class="otp-container" @paste.prevent="handlePaste">
        <input
          v-for="(val, i) in otpValues"
          :key="i"
          type="text"
          maxlength="1"
          v-model="otpValues[i]"
          ref="inputRefs[i]"
          @input="e => handleInput(e, i)"
          @keydown="e => handleKeydown(e, i)"
          class="otp-input"
        />
      </div>

      <button class="verify-btn" @click="verifyOTP" :disabled="loading">
        {{ loading ? 'Verifying...' : 'Verify' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal {
  background: white;
  padding: 2em;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}
.otp-container {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  margin: 20px 0;
}
.otp-input {
  width: 50px;
  height: 60px;
  text-align: center;
  font-size: 1.8em;
  border: 2px solid #ccc;
  border-radius: 10px;
  transition: border 0.2s;
}
.otp-input:focus {
  outline: none;
  border-color: #04724D;
}
.verify-btn {
  background: #04724D;
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 1em;
  border-radius: 8px;
  cursor: pointer;
}
.verify-btn:hover {
  background: #035e3c;
}
</style>
