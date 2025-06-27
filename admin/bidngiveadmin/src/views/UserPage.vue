<template>
  <div class="user-page">
    <section class="content">
      <h2>👥 Registered Users</h2>
      <table class="user-table" v-if="users.length">
        <thead>
          <tr>
            <th>#</th>
            <th>Username</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, index) in users" :key="user.id">
            <td>{{ index + 1 }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.phone_number }}</td>
            <td>
              <span :class="user.is_disabled ? 'blocked' : 'active'">
                {{ user.is_disabled ? 'Blocked' : 'Active' }}
              </span>
            </td>
            <td>
              <button @click="blockUser(user.email)" class="danger">Block</button>
              <button @click="unblockUser(user.email)" class="success">Unblock</button>
              <button @click="loginAs(user.email)" class="primary">Login</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>Loading users...</p>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const users = ref([])
const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchUsers = async () => {
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/admin/admin/all-users/', { headers })
    users.value = res.data
  } catch {
    toast.error('Failed to fetch users')
  }
}

const blockUser = async (email) => {
  try {
    await axios.post('https://bidngive.onrender.com/api/admin/user/block/', { email }, { headers })
    toast.success('User blocked')
    fetchUsers()
  } catch {
    toast.error('Failed to block user')
  }
}

const unblockUser = async (email) => {
  try {
    await axios.post('https://bidngive.onrender.com/api/admin/user/unblock/', { email }, { headers })
    toast.success('User unblocked')
    fetchUsers()
  } catch {
    toast.error('Failed to unblock user')
  }
}

const loginAs = async (email) => {
  try {
    const res = await axios.post('https://bidngive.onrender.com/api/admin/user/login-as/', { email }, { headers })
    localStorage.setItem('access_token', res.data.access)
    localStorage.setItem('refresh_token', res.data.refresh)
    localStorage.setItem('userInfo', JSON.stringify({ username: res.data.username, email: res.data.email }))
    window.location.href = '/'
  } catch {
    toast.error('Failed to login as user')
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.user-page {
  background: #f5f5f5;
  min-height: 100vh;
}
.content {
  padding: 32px;
}
.user-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}
.user-table th,
.user-table td {
  padding: 14px 18px;
  text-align: left;
  border-bottom: 1px solid #eee;
}
button {
  padding: 6px 14px;
  margin-right: 5px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}
.danger {
  background: #d32f2f;
  color: white;
}
.success {
  background: #388e3c;
  color: white;
}
.primary {
  background: #1565c0;
  color: white;
}
.active {
  color: green;
  font-weight: 600;
}
.blocked {
  color: red;
  font-weight: 600;
}
</style>
