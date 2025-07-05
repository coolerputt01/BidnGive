<template>
  <main class="manual-merge-container">
    <h1>🔄 Manual Merge Bids</h1>
    <p class="subtitle">
      Select <strong>1 withdrawal bid (seller)</strong> and matching <strong>investment bids (buyers)</strong>.
    </p>

    <div v-if="loading" class="loader">Loading bids…</div>

    <div v-else>
      <!-- Withdrawal Seller Section -->
      <h3 class="section-title">🔴 Seller Withdrawal Investment</h3>
      <table class="bids-table">
        <thead>
          <tr>
            <th>Select</th>
            <th>User</th>
            <th>Amount</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="bid in withdrawalBids"
            :key="bid.id"
          >
            <td>
              <input
                type="checkbox"
                :value="bid"
                v-model="selectedBids"
                :disabled="isChecked(bid) ? false : selectedWithdrawal.length === 1"
              />
            </td>
            <td>{{ bid.username }}</td>
            <td>{{ formatAmount(bid.amount) }}</td>
            <td>{{ formatDate(bid.created) }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Buyers Section -->
      <h3 class="section-title">🟢 Buyer Investment Bids</h3>
      <table class="bids-table">
        <thead>
          <tr>
            <th>Select</th>
            <th>User</th>
            <th>Amount</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="bid in investmentBids"
            :key="bid.id"
          >
            <td>
              <input
                type="checkbox"
                :value="bid"
                v-model="selectedBids"
              />
            </td>
            <td>{{ bid.username }}</td>
            <td>{{ formatAmount(bid.amount) }}</td>
            <td>{{ formatDate(bid.created) }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Matching Info -->
      <div class="merge-check">
        <p><strong>Buyer Total:</strong> ₦{{ totalInvestment.toLocaleString() }}</p>
        <p><strong>Seller Amount:</strong> ₦{{ totalWithdrawal.toLocaleString() }}</p>
        <p><strong>Ready to Merge:</strong>
          <span :class="canMerge ? 'ready' : 'not-ready'">{{ canMerge ? '✅ Yes' : '❌ No' }}</span>
        </p>
      </div>

      <!-- Merge Button -->
      <button
        class="merge-button"
        :disabled="!canMerge || merging"
        @click="handleMerge"
      >
        <span v-if="merging">Merging...</span>
        <span v-else>Merge Selected Bids</span>
      </button>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

const bids = ref([])
const selectedBids = ref([])
const loading = ref(true)
const merging = ref(false)

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchPendingBids = async () => {
  loading.value = true
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/admin/pending-bids/', { headers })
    bids.value = res.data
    console.log(bids.value)
  } catch {
    toast.error('Failed to load pending bids.')
  } finally {
    loading.value = false
  }
}

const isEligible = (bid) => {
  return (
    (bid.status === 'awaiting') ||
    bid.admin_paid === true
  )
}

const withdrawalBids = computed(() =>
  bids.value.filter(b => b.type === 'withdrawal' && isEligible(b))
)

const investmentBids = computed(() =>
  bids.value.filter(b => b.type === 'investment' && isEligible(b))
)

console.log(withdrawalBids)

const selectedWithdrawal = computed(() => selectedBids.value.filter(b => b.type === 'withdrawal'))
const selectedInvestment = computed(() => selectedBids.value.filter(b => b.type === 'investment'))

const totalInvestment = computed(() => selectedInvestment.value.reduce((sum, b) => sum + parseFloat(b.amount), 0))
const totalWithdrawal = computed(() => selectedWithdrawal.value.reduce((sum, b) => sum + parseFloat(b.amount), 0))

const canMerge = computed(() => {
  return (
    selectedWithdrawal.value.length === 1 &&
    selectedInvestment.value.length > 0 &&
    totalInvestment.value === totalWithdrawal.value
  )
})

const handleMerge = async () => {
  if (!canMerge.value) return
  merging.value = true
  try {
    const bidIds = selectedBids.value.map(b => b.id)
    const res = await axios.post(
      'https://bidngive.onrender.com/api/admin/merge/manual/',
      { bid_ids: bidIds },
      { headers }
    )
    toast.success(res.data.message || 'Merged successfully.')
    selectedBids.value = []
    fetchPendingBids()
  } catch (err) {
    toast.error(err.response?.data?.error || 'Merge failed.')
  } finally {
    merging.value = false
  }
}

const formatDate = (iso) => new Date(iso).toLocaleString('en-GB', {
  day: '2-digit', month: 'short', year: 'numeric',
  hour: '2-digit', minute: '2-digit'
})

const formatAmount = (num) =>
  Number(num).toLocaleString('en-NG', {
    minimumFractionDigits: 2, maximumFractionDigits: 2
  })

const isChecked = (bid) => selectedBids.value.some(b => b.id === bid.id)

onMounted(fetchPendingBids)
</script>

<style scoped>
.manual-merge-container {
  max-width: 960px;
  margin: 2rem auto;
  background: white;
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 0 12px rgba(0,0,0,0.05);
  font-family: 'Segoe UI', sans-serif;
}

h1 {
  font-size: 1.8rem;
  color: #17a35e;
  margin-bottom: 0.25rem;
}
.subtitle {
  margin-bottom: 1.2rem;
  color: #555;
}

.section-title {
  margin-top: 1.5rem;
  margin-bottom: 0.8rem;
  font-size: 1.1rem;
  font-weight: bold;
  color: #222;
}

.bids-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}
.bids-table th,
.bids-table td {
  padding: 10px 14px;
  border-bottom: 1px solid #eee;
  text-align: left;
}
.bids-table th {
  background: #f6fef9;
  color: #0a7046;
}
.bids-table tbody tr:hover {
  background-color: #f9fffc;
}

.merge-check {
  text-align: center;
  margin: 1rem 0;
  font-size: 1rem;
}

.ready {
  color: green;
  font-weight: bold;
}
.not-ready {
  color: red;
  font-weight: bold;
}

.merge-button {
  display: block;
  margin: 0 auto;
  margin-top: 12px;
  padding: 12px 28px;
  background-color: #17a35e;
  color: white;
  border: none;
  border-radius: 28px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
}
.merge-button:disabled {
  background-color: #a2d5a0;
  cursor: not-allowed;
}
.merge-button:not(:disabled):hover {
  background-color: #128f4a;
}
</style>
