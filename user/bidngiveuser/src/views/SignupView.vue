<script setup>
import { useRouter } from 'vue-router';
import { toast } from 'vue3-toastify';

const router = useRouter();
const notify = () => {
  toast("Wow so easy !", {
    autoClose: 1000,
    position: toast.POSITION.TOP_RIGHT,
  });
}
toast.success("Wow so easy !", {
    autoClose: 1000,
    position: toast.POSITION.TOP_RIGHT,
  });
</script>

<template>
  <main style="background-color: #EBEBD3;width:100vw;height: 100vh;overflow-x: hidden;">
      <section style="display: flex;justify-content: center;align-items: center;width: 100%;height: 100%;">
        <form style="background-color: #fff;border-radius: 13px;padding: 3%;width: 70%;height: 80%;box-shadow: 10px 10px 32px -13px rgba(0,0,0,0.1657);display: flex;justify-content: space-between;align-items: center;">
          <section style="width: 100%;">
            <div>
              <h1 style="font-size: 2em;font-weight: 650;">Signup</h1>
            </div>
            <div class="inputs" style="margin-top: 3%;">
              <div class="input-val" style="display: flex;justify-content: flex-start;align-items: center;border-bottom: 2px solid grey;width: 50%;">
                <label for="fullname"><img src="/icons/person.svg" alt="Person Fullname" style="width: 1.2em;height: 1.2em;"></label>
                <input type="text" placeholder="Your Fullname" style="outline: none;border: none;padding: 12px;width: 100%;font-size: 1em;">
              </div>

              <div class="input-val" style="display: flex;justify-content: flex-start;align-items: center;border-bottom: 2px solid grey;width: 50%;">
                <label for="email"><img src="/icons/email.svg" alt="Person Email" style="width: 1.2em;height: 1.2em;"></label>
                <input type="email" placeholder="Your Email" style="outline: none;border: none;padding: 12px;width: 100%;font-size: 1em;">
              </div>

              <div class="input-val" style="display: flex;justify-content: flex-start;align-items: center;border-bottom: 2px solid grey;width: 50%;">
                <label for="phoneNumber"><img src="/icons/phone.svg" alt="Person Phone number" style="width: 1.2em;height: 1.2em;"></label>
                <input type="text" placeholder="Your Phone number" style="outline: none;border: none;padding: 12px;width: 100%;font-size: 1em;">
              </div>

              <div class="input-val" style="display: flex;justify-content: flex-start;align-items: center;border-bottom: 2px solid grey;width: 50%;">
                <label for="password"><img src="/icons/lock-closed.svg" alt="Person Password" style="width: 1.2em;height: 1.2em;"></label>
                <input type="password" placeholder="Your Password" style="outline: none;border: none;padding: 12px;width: 100%;font-size: 1em;" minlength="6">
              </div>

              <div class="input-val" style="display: flex;justify-content: flex-start;align-items: center;border-bottom: 2px solid grey;width: 50%;">
                <label for="password"><img src="/icons/locked.svg" alt="Person Password" style="width: 1.2em;height: 1.2em;"></label>
                <input type="password" placeholder="Repeat your password" style="outline: none;border: none;padding: 12px;width: 100%;font-size: 1em;" minlength="6">
              </div>
              <div style="margin-top: 5%;">
                <input type="checkbox" name="agreement"><label for="agreement">I agree all statements in <a href="#" @click="router.push('terms-of-service')">Terms of service</a></label>
              </div>
              <div style="display: flex;justify-content: flex-start;align-items: center;">
                <button style="width: 25vw;height: 3em;color: #fff;outline: none;border: none;background-color: #04724D;cursor: pointer;text-align: center;display: flex;justify-content: center;align-items: center;" @click.prevent="notify()">
                  <span>Register</span>
                  <!-- <div class="loader"></div> -->
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