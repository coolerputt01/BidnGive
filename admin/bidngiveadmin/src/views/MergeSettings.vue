<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { toast } from 'vue3-toastify';

const morning = ref('');
const evening = ref('');
const loading = ref(false);
const token = localStorage.getItem("access_token");
const headers = { Authorization: `Bearer ${token}` };

const fetchSettings = async () => {
  try {
    const res = await axios.get("https://bidngive.onrender.com/api/admin/merge/settings/", { headers });
    morning.value = res.data.morning_time;
    evening.value = res.data.evening_time;
  } catch (err) {
    toast.error("Failed to load settings");
  }
};

const updateSettings = async () => {
  loading.value = true;
  try {
    await axios.patch("https://bidngive.onrender.com/api/admin/merge/settings/", {
      morning_time: morning.value,
      evening_time: evening.value
    }, { headers });
    toast.success("Merge settings updated!");
  } catch (err) {
    toast.error("Failed to update settings");
  } finally {
    loading.value = false;
  }
};

onMounted(fetchSettings);
</script>

<template>
  <main class="settings-container">
    <h2>⏱ Update Merge Auction Times</h2>
    <div class="settings-form">
      <label>
        Morning Time:
        <input type="time" v-model="morning" />
      </label>
      <label>
        Evening Time:
        <input type="time" v-model="evening" />
      </label>
      <button :disabled="loading" @click="updateSettings">
        {{ loading ? 'Saving...' : 'Update Settings' }}
      </button>
    </div>
  </main>
</template>

<style scoped>
.settings-container {
  max-width: 500px;
  margin: 40px auto;
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.settings-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}
label {
  display: flex;
  justify-content: space-between;
  font-weight: 600;
  color: #333;
}
input[type="time"] {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
button {
  padding: 10px;
  background: #04724D;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
}
button:hover {
  background-color: #03563a;
}
</style>
