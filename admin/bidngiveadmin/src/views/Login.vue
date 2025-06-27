<template>
  <main class="login-container">
    <div class="login-card">
      <h2>Admin Login</h2>
      <p class="subtext">Sign in to your admin dashboard</p>

      <form @submit.prevent="loginAdmin" class="form">
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="admin@example.com" required />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input v-model="form.password" type="password" placeholder="••••••••" required />
        </div>

        <button type="submit" :disabled="loading" class="btn">
          <span v-if="!loading">Login</span>
          <span v-else>Logging in...</span>
        </button>
      </form>
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
  email: '',
  password: '',
})

const loginAdmin = async () => {
  loading.value = true
  try {
    const res = await axios.post('https://bidngive.onrender.com/api/accounts/token/', form.value)
    localStorage.setItem('access_token', res.data.access)

    const userInfo = await axios.get('https://bidngive.onrender.com/api/accounts/me/', {
        headers: { Authorization: `Bearer ${token}` }
    });

    if (!userInfo.data.is_staff) {
        toast.error("Access denied. Not an admin.");
        localStorage.removeItem("access_token");
        return;
    }
    toast.success('Login successful!')

    router.push('/admin-dashboard')
  } catch (err) {
    toast.error('Invalid login credentials')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  background-color: #ebebd3;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
}

.login-card h2 {
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
