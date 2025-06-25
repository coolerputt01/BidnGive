<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router';
import { toast } from 'vue3-toastify';
import axios from 'axios';

const router = useRouter();
const apiUrl = "https://bidngive.onrender.com/api/accounts/register/";

const username = ref('')
const email = ref('')
const phone_number = ref('')
const password = ref('')
const confirmPassword = ref('')
const referral_code = ref('')
const loading = ref(false)

const signUp = async () => {
  if (password.value !== confirmPassword.value) {
    toast.error("Passwords do not match!")
    return
  }

  loading.value = true

  try {
    const response = await axios.post(apiUrl, {
      username: username.value,
      email: email.value,
      phone_number: phone_number.value,
      password: password.value,
      referral_code: referral_code.value || undefined
    })

    toast.success("Account created! Redirecting...", {
      autoClose: 1000,
      position: toast.POSITION.TOP_RIGHT
    })
    console.log(response.data)

    setTimeout(() => {
    localStorage.setItem("userInfo", JSON.stringify({
      username: username.value,
      email: email.value,
    }));
      router.push('/otp');
    }, 1500)
  } catch (error) {
    if (error.response?.data) {
      for (const [key, messages] of Object.entries(error.response.data)) {
        toast.error(`${key}: ${messages[0]}`)
      }
    } else {
      toast.error("An error occurred. Please try again.")
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main style="background-color: #EBEBD3;width:100vw;height: 100vh;overflow-x: hidden;">
      <section style="display: flex;justify-content: center;align-items: center;width: 100%;height: 100%;">
        <form style="background-color: #fff;border-radius: 13px;padding: 3%;width: 70%;height: 90%;box-shadow: 10px 10px 32px -13px rgba(0,0,0,0.1657);display: flex;justify-content: space-between;align-items: center;">
          <section style="width: 100%;">
            <div>
              <h1 style="font-size: 2em;font-weight: 650;">Signup</h1>
            </div>
            <div class="inputs" style="margin-top: 3%;">
              <div class="input-val" style="display: flex;justify-content: flex-start;align-items: center;border-bottom: 2px solid grey;width: 50%;">
                <label for="fullname"><img src="/icons/person.svg" alt="Person Fullname" style="width: 1.2em;height: 1.2em;"></label>
                <input type="text" v-model="username" placeholder="Your Fullname" style="outline: none;border: none;padding: 12px;width: 100%;font-size: 1em;">
              </div>

              <div class="input-val" style="display: flex;justify-content: flex-start;align-items: center;border-bottom: 2px solid grey;width: 50%;">
                <label for="email"><img src="/icons/email.svg" alt="Person Email" style="width: 1.2em;height: 1.2em;"></label>
                <input type="email" v-model="email" placeholder="Your Email" style="outline: none;border: none;padding: 12px;width: 100%;font-size: 1em;">
              </div>

              <div class="input-val" style="display: flex;justify-content: flex-start;align-items: center;border-bottom: 2px solid grey;width: 50%;">
                <label for="phoneNumber"><img src="/icons/phone.svg" alt="Person Phone number" style="width: 1.2em;height: 1.2em;"></label>
                <input type="text" v-model="phone_number" placeholder="Your Phone number" style="outline: none;border: none;padding: 12px;width: 100%;font-size: 1em;" maxlength="11">
              </div>

              <div class="input-val" style="display: flex;justify-content: flex-start;align-items: center;border-bottom: 2px solid grey;width: 50%;">
                <label for="password"><img src="/icons/lock-closed.svg" alt="Person Password" style="width: 1.2em;height: 1.2em;"></label>
                <input type="password" v-model="password" placeholder="Your Password" style="outline: none;border: none;padding: 12px;width: 100%;font-size: 1em;" minlength="6">
              </div>

              <div class="input-val" style="display: flex;justify-content: flex-start;align-items: center;border-bottom: 2px solid grey;width: 50%;">
                <label for="password"><img src="/icons/locked.svg" alt="Person Password" style="width: 1.2em;height: 1.2em;"></label>
                <input type="password" v-model="confirmPassword" placeholder="Repeat your password" style="outline: none;border: none;padding: 12px;width: 100%;font-size: 1em;" minlength="6">
              </div>
              <div class="input-val" style="display: flex;justify-content: flex-start;align-items: center;border-bottom: 2px solid grey;width: 50%;">
                <label for="referral"><img src="/icons/person.svg" alt="Person Referral Code" style="width: 1.2em;height: 1.2em;"></label>
                <input type="text" v-model="referral_code" placeholder="Referral Code" style="outline: none;border: none;padding: 12px;width: 100%;font-size: 1em;" minlength="6">
              </div>
              <div style="margin-top: 5%;">
                <input type="checkbox" name="agreement"><label for="agreement">I agree all statements in <a href="#" @click="router.push('terms-of-service')">Terms of service</a></label>
              </div>
              <div style="display: flex;justify-content: flex-start;align-items: center;">
                <button style="width: 25vw;height: 3em;color: #fff;outline: none;border: none;background-color: #04724D;cursor: pointer;text-align: center;display: flex;justify-content: center;align-items: center;" @click.prevent="signUp" :disabled="loading">
                  <span v-if="!loading">Register</span>
                  <div v-else class="loader"></div>
                </button>
              </div>
              <div class="redirect" style="font-size: 0.9em;text-align: left;width: 100%;margin-top: 5%;">Already have an account?<a href="#" @click="router.push('/')"> Login</a></div>
            </div>
          </section>
        </form>
      </section>
  </main>
</template>

<style scoped>
input::placeholder {
  margin-left: 0.4em;
}
.inputs > *{
  margin-bottom: 2%;
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
@media (max-width:480px) {
  form {
    width: 100% !important;
    height: 60% !important;
  }
  .redirect {
    width: 100% !important;
  }
  .input-val {
    width: 70% !important;
  }
}
</style>