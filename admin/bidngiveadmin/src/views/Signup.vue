<template>
  <main class="register-container">
    <div class="register-card">
      <h2>Create Admin Account</h2>
      <p class="subtext">Register to access the admin dashboard</p>

      <form @submit.prevent="registerAdmin" class="form">
        <div class="form-group">
          <label>Username</label>
          <input v-model="form.username" type="text" placeholder="adminuser" required />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="admin@example.com" required />
        </div>

        <div class="form-group">
          <label>Phone Number</label>
          <input v-model="form.phone_number" type="tel" placeholder="08012345678" required />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input v-model="form.password" type="password" placeholder="••••••••" required />
        </div>

        <button type="submit" :disabled="loading" class="btn">
          <span v-if="!loading">Register</span>
          <span v-else>Processing...</span>
        </button>
      </form>

      <p class="footer-text">
        Already have an account?
        <router-link to="/admin-login">Login here</router-link>
      </p>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify'

const router = useRouter()
const loading = ref(false)

const form = ref({
  username: '',
  email: '',
  phone_number: '',
  password: ''
})

const registerAdmin = async () => {
  loading.value = true
  try {
    const response = await axios.post('https://bidngive.onrender.com/api/accounts/register/', {
      ...form.value,
      is_staff: true, // Ensure admin flag
      is_email_verified: true,
      is_phone_verified: true
    })

    toast.success('Admin registered! Please login.')
    setTimeout(() => router.push('/admin-login'), 1500)
  } catch (error) {
    const errMsg = error.response?.data?.error || 'Registration failed.'
    toast.error(errMsg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  background-color: #ebebd3;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
}

.register-card h2 {
  font-size: 1.8em;
  font-weight: 600;
  color: #191919;
  text-align: center;
  margin-bottom: 0.25em;
}

.subtext {
  text-align: center;
  font-size: 0.9em;
  color: gray;
  margin-bottom: 2rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-size: 0.9em;
  margin-bottom: 0.4em;
  color: #444;
}

input {
  padding: 0.7em;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1em;
  transition: border-color 0.3s ease;
}

input:focus {
  border-color: #04724d;
  outline: none;
}

.btn {
  background-color: #04724d;
  color: white;
  padding: 0.75em;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #03573b;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.footer-text {
  text-align: center;
  font-size: 0.85em;
  color: gray;
  margin-top: 1.8rem;
}

.footer-text a {
  color: #04724d;
  text-decoration: none;
  font-weight: 600;
  margin-left: 5px;
}

.footer-text a:hover {
  text-decoration: underline;
}
</style>
