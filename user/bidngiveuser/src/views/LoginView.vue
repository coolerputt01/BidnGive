<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { toast } from 'vue3-toastify';
import axios from 'axios';

const router = useRouter();
const username = ref('');
const password = ref('');
const loading = ref(false);

const login = async () => {
  if (!username.value || !password.value) {
    toast.error("Both fields are required");
    return;
  }

  loading.value = true;

  try {
    const response = await axios.post("https://bidngive.onrender.com/api/accounts/login/", {
      email: username.value,
      password: password.value,
    });

    const { access, refresh, is_phone_verified } = response.data;

    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    localStorage.setItem("userInfo", JSON.stringify({ username: username.value }));

    if (!is_phone_verified) {
      await axios.post("https://bidngive.onrender.com/api/accounts/send-whatsapp-otp/", {}, {
        headers: { Authorization: `Bearer ${access}` }
      });
      toast.success("OTP sent to your WhatsApp.");
    }

    toast.success("Login successful!");
    setTimeout(() => {
      router.push('/dashboard')
    }, 200)
  } catch (err) {
    toast.error("Invalid credentials or user does not exist");
    console.log("hi")
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <main class="page">
    <div class="form-wrapper">
      <header class="form-header">
        <div class="logo">Bidn<span>Give</span></div>
        <h1>Sign In</h1>
        <p>Login to your account</p>
      </header>

      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <input v-model="username" type="text" id="email" required placeholder=" " />
          <label for="email">Email</label>
        </div>

        <div class="form-group">
          <input v-model="password" type="password" id="password" minlength="6" required placeholder=" " />
          <label for="password">Password</label>
        </div>

        <button :disabled="loading" class="submit-btn">
          <span v-if="!loading">Login</span>
          <span v-else class="loader"></span>
        </button>

        <p class="redirect">
          Don’t have an account?
          <a @click.prevent="router.push('/signup')">Sign up</a>
        </p>
      </form>
    </div>
  </main>
</template>

<style scoped>
.page {
  height: 100vh;
  width: 100vw;
  background-color: #fdfdfc; /* clean solid tone */
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Segoe UI', sans-serif;
}

.form-wrapper {
  width: 100%;
  max-width: 400px;
  padding: 1rem 2rem;
  display: flex;
  flex-direction: column;
}

.logo {
  font-size: 1.8rem;
  font-weight: 700;
  color: #04724D;
  margin-bottom: 0.5rem;
  letter-spacing: 0.5px;
}
.logo span {
  color: #222;
}
.form-header {
  width: 100%;
}
.form-header > * {
  text-align: center !important;
}

.form-header h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #222;
  margin-bottom: 0.2rem;
}

.form-header p {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 1.8rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  position: relative;
  width: 100%;
}

.form-group input {
  width: 100%;
  padding: 1.1rem 0.75rem 0.5rem;
  font-size: 1rem;
  border: none;
  border-bottom: 2px solid #ccc;
  background: transparent;
  outline: none;
  transition: all 0.2s ease;
}

.form-group label {
  position: absolute;
  top: 1rem;
  left: 0.75rem;
  font-size: 1rem;
  color: #777;
  pointer-events: none;
  transition: all 0.2s ease;
}

.form-group input:focus + label,
.form-group input:not(:placeholder-shown) + label {
  top: 0.3rem;
  font-size: 0.8rem;
  color: #04724D;
}

.form-group input:focus {
  border-bottom: 2px solid #04724D;
}

.submit-btn {
  background-color: #04724D;
  color: white;
  padding: 0.9rem;
  font-size: 1rem;
  font-weight: 500;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.submit-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.loader {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.redirect {
  text-align: center;
  font-size: 0.9rem;
  color: #555;
  margin-top: 1rem;
}

.redirect a {
  color: #04724D;
  font-weight: 600;
  margin-left: 4px;
  cursor: pointer;
}
</style>
