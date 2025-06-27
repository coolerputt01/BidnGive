<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { toast } from 'vue3-toastify';

const email = ref('');
const token = localStorage.getItem("access_token");
const headers = { Authorization: `Bearer ${token}` };

const blockUser = async () => {
  try {
    await axios.post("https://bidngive.onrender.com/api/admin/user/block/", { email: email.value }, { headers });
    toast.success(`${email.value} blocked successfully.`);
  } catch (err) {
    toast.error(err.response?.data?.error || "Failed to block user");
  }
};

const unblockUser = async () => {
  try {
    await axios.post("https://bidngive.onrender.com/api/admin/user/unblock/", { email: email.value }, { headers });
    toast.success(`${email.value} unblocked successfully.`);
  } catch (err) {
    toast.error(err.response?.data?.error || "Failed to unblock user");
  }
};

const loginAsUser = async () => {
  try {
    const res = await axios.post("https://bidngive.onrender.com/api/admin/user/login-as/", { email: email.value }, { headers });
    localStorage.setItem("access_token", res.data.access);
    localStorage.setItem("refresh_token", res.data.refresh);
    localStorage.setItem("userInfo", JSON.stringify({ username: res.data.username, email: res.data.email }));
    toast.success(`Logged in as ${res.data.username}`);
    window.location.href = "/"; // Redirect to user dashboard
  } catch (err) {
    toast.error(err.response?.data?.error || "Login failed");
  }
};
</script>

<template>
  <main class="management-container">
    <h2>🔒 User Management</h2>
    <input type="email" v-model="email" placeholder="Enter user email" class="input" />

    <div class="btn-group">
      <button @click="blockUser" class="danger">Block</button>
      <button @click="unblockUser" class="success">Unblock</button>
      <button @click="loginAsUser" class="primary">Login as User</button>
    </div>
  </main>
</template>

<style scoped>
.management-container {
  max-width: 600px;
  margin: 40px auto;
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.input {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.btn-group {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}
button {
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
.danger {
  background: #c62828;
  color: white;
}
.success {
  background: #2e7d32;
  color: white;
}
.primary {
  background: #1565c0;
  color: white;
}
</style>
