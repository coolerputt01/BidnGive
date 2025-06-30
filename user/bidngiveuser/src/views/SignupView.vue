<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { toast } from 'vue3-toastify';
import axios from 'axios';

const router = useRouter();

const apiUrl = "https://bidngive.onrender.com/api/accounts/register/";
const eye = '/icons/eye-svgrepo-com.svg';
const eyeClosed = '/icons/eye-slash-svgrepo-com.svg';

const showPassword = ref(false);
const showConfirmPassword = ref(false);

const username = ref('');
const email = ref('');
const phone_number = ref('');
const password = ref('');
const confirmPassword = ref('');
const referral_code = ref('');
const loading = ref(false);

onMounted(() => {
  // Handle referral from hash URL (e.g. #/signup?ref=REFZEE)
  const hash = window.location.hash;
  const queryString = hash.includes('?') ? hash.split('?')[1] : '';
  const params = new URLSearchParams(queryString);
  const referralFromUrl = params.get('ref');

  if (referralFromUrl) {
    referral_code.value = referralFromUrl;
    localStorage.setItem('referral', referralFromUrl);
  } else {
    const storedReferral = localStorage.getItem('referral');
    if (storedReferral) {
      referral_code.value = storedReferral;
    }
  }
});

const signUp = async () => {
  if (password.value !== confirmPassword.value) {
    toast.error("Passwords do not match!");
    return;
  }

  loading.value = true;

  try {
    await axios.post(apiUrl, {
      username: username.value,
      email: email.value,
      phone_number: phone_number.value,
      password: password.value,
      referral_code: referral_code.value || undefined,
    });

    toast.success("Account created! Redirecting...");

    localStorage.setItem("userInfo", JSON.stringify({
      username: username.value,
      email: email.value,
    }));

    localStorage.removeItem('referral');

    setTimeout(() => {
      router.push('/otp');
    }, 1500);
  } catch (error) {
    if (error.response?.data) {
      for (const [key, messages] of Object.entries(error.response.data)) {
        toast.error(`${key}: ${messages[0]}`);
      }
    } else {
      toast.error("An error occurred. Please try again.");
    }
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
        <h1>Create an Account</h1>
        <p>Join the BidnGive community</p>
      </header>

      <form class="login-form" @submit.prevent="signUp">
        <div class="form-group"><input v-model="username" type="text" required placeholder=" " /><label>Username</label></div>
        <div class="form-group"><input v-model="email" type="email" required placeholder=" " /><label>Email</label></div>
        <div class="form-group"><input v-model="phone_number" type="text" required placeholder=" " maxlength="11" /><label>Phone Number</label></div>

        <div class="form-group password-field">
          <input :type="showPassword ? 'text' : 'password'" v-model="password" required placeholder=" " minlength="6" />
          <label>Password</label>
          <span class="toggle-icon" @click="showPassword = !showPassword">
            <img :src="showPassword ? eye : eyeClosed" alt="toggle password" />
          </span>
        </div>

        <div class="form-group password-field">
          <input :type="showConfirmPassword ? 'text' : 'password'" v-model="confirmPassword" required placeholder=" " minlength="6" />
          <label>Confirm Password</label>
          <span class="toggle-icon" @click="showConfirmPassword = !showConfirmPassword">
            <img :src="showConfirmPassword ? eye : eyeClosed" alt="toggle password" />
          </span>
        </div>

        <div class="form-group">
          <input v-model="referral_code" type="text" placeholder=" " />
          <label>Referral Code (optional)</label>
        </div>

        <div class="checkbox">
          <input type="checkbox" id="tos" required />
          <label for="tos">I agree to the <a @click.prevent="router.push('/terms-of-service')">Terms of Service</a></label>
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          <span v-if="!loading">Register</span>
          <span v-else class="loader"></span>
        </button>

        <p class="redirect">
          Already have an account?
          <a @click.prevent="router.push('/')">Login</a>
        </p>
      </form>
    </div>
  </main>
</template>

<style scoped>
.page {
  height: 100vh;
  width: 100vw;
  background-color: #fdfdfc;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Segoe UI', sans-serif;
}
.toggle-icon img {
  width: 20px;
  height: 20px;
}

.password-field {
  position: relative;
}

.toggle-icon {
  position: absolute;
  top: 50%;
  right: 0.75rem;
  transform: translateY(-50%);
  font-size: 1.1rem;
  cursor: pointer;
  color: #888;
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
  gap: 1.4rem;
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

.checkbox {
  font-size: 0.9rem;
  color: #555;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox a {
  color: #04724D;
  font-weight: 500;
  text-decoration: underline;
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
  to { transform: rotate(360deg); }
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
