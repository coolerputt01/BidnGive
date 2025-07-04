<template>
  <main class="referral-page">
    <section class="header">
      <h1>👥 Your Referred Users</h1>
      <p>Below is a list of all users who signed up using your referral code.</p>
    </section>

    <div v-if="loading" class="loading">Loading downlines...</div>

    <section v-else>
      <div v-if="downlines.length" class="table-wrapper">
        <table class="downline-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Username</th>
              <th>Email</th>
              <th>Joined</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in downlines" :key="user.id">
              <td>{{ index + 1 }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ formatDate(user.date_joined) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="empty-state">
        <img src="/images/notfound.gif" alt="No Downlines" />
        <h2>No Downlines Yet</h2>
        <p>You haven’t referred anyone yet. Share your referral link and earn bonuses!</p>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const downlines = ref([])
const loading = ref(true)

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchDownlines = async () => {
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/accounts/my-downlines/', { headers })
    downlines.value = res.data
  } catch (err) {
    console.error('Failed to load downlines', err)
  } finally {
    loading.value = false
  }
}

const formatDate = (iso) => {
  const d = new Date(iso)
  return d.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

onMounted(fetchDownlines)
</script>

<style scoped>
.referral-page {
  max-width: 900px;
  margin: 40px auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}
.header h1 {
  font-size: 1.8rem;
  color: #004f28;
}
.header p {
  color: #555;
  font-size: 1rem;
}

.loading {
  text-align: center;
  font-size: 1.1rem;
  color: #888;
  margin-top: 50px;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  background: white;
}

.downline-table {
  width: 100%;
  border-collapse: collapse;
}
.downline-table th,
.downline-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #eee;
  text-align: left;
}
.downline-table th {
  background-color: #e7f7ef;
  color: #04724D;
  font-weight: 600;
}

.downline-table tbody tr:hover {
  background-color: #f9f9f9;
}

.empty-state {
  text-align: center;
  margin-top: 50px;
}
.empty-state img {
  width: 240px;
  max-width: 80%;
  margin-bottom: 20px;
}
.empty-state h2 {
  font-size: 1.4rem;
  color: #444;
}
.empty-state p {
  font-size: 0.95rem;
  color: #777;
  margin-top: 6px;
}
</style>
