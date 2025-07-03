<template>
  <section class="create-bid">
    <h2 class="page-title">Create Investment Bid</h2>

    <form class="create-form" @submit.prevent="submitBid">
      <label for="amount">Amount (₦):</label>
      <input type="number" id="amount" v-model="form.amount" required />
      <span>Min: ₦10,000 Max: ₦500,000</span>

      <div v-if="form.amount" class="live-summary">
        <p><strong>📈 Expected Return:</strong> ₦{{ expectedReturn }}</p>
        <p><strong>💹 Profit:</strong> ₦{{ profitAmount }}</p>
        <p><strong>⏳ Duration:</strong> 24 hours</p>
        <p><strong>🔁 Recommitment:</strong> 100% mandatory</p>
      </div>

      <button type="submit" :disabled="loadingSubmit || userHasPendingBid">
        {{ userHasPendingBid ? 'Pending Bid Exists' : 'Create Investment Bid' }}
      </button>
    </form>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { toast } from 'vue3-toastify';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const token = localStorage.getItem('access_token');
const form = ref({ amount: '' });
const loadingSubmit = ref(false);
const bids = ref([]);
const currentUserId = ref(null);

const fetchProfile = async () => {
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/accounts/me/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    currentUserId.value = res.data.id;
  } catch (err) {
    console.error('Profile fetch failed', err);
  }
};

const fetchBids = async () => {
  try {
    const res = await axios.get('https://bidngive.onrender.com/api/bids/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    bids.value = res.data;
  } catch (err) {
    console.error('Bids fetch failed', err);
  }
};

const userHasPendingBid = computed(() => {
  return bids.value.some(
    bid =>
      bid.user === currentUserId.value &&
      bid.status !== 'paid' &&
      bid.status !== 'cancelled' &&
      bid.status !== 'confirmed'
  );
});

const expectedReturn = computed(() => {
  const amt = parseFloat(form.value.amount || 0);
  return amt > 0 ? Math.round(amt * 1.5).toLocaleString() : '0';
});

const profitAmount = computed(() => {
  const amt = parseFloat(form.value.amount || 0);
  return amt > 0 ? Math.round(amt * 0.5).toLocaleString() : '0';
});

const submitBid = async () => {
  if (loadingSubmit.value) return;

  const amount = parseFloat(form.value.amount);
  if (isNaN(amount) || amount < 10000 || amount > 500000) {
    toast.error('Amount must be between ₦10,000 and ₦500,000');
    return;
  }

  loadingSubmit.value = true;
  try {
    await axios.post('https://bidngive.onrender.com/api/bids/', {
      amount,
      plan: '50_24',
      
    }, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    toast.success('🎉 Bid successfully created!');
    form.value.amount = '';
    router.push('/bid');
  } catch (err) {
    toast.error('❌ Failed to create bid.');
  } finally {
    loadingSubmit.value = false;
  }
};

onMounted(async () => {
  await fetchProfile();
  await fetchBids();
});
</script>
<style scoped>
.create-bid {
  background-color: #f4f4f4;
  padding: 20px;
  font-family: 'Segoe UI', sans-serif;
}

.page-title {
  font-size: 1.4em;
  font-weight: bold;
  text-align: center;
  margin-bottom: 1em;
  color: #191919;
}

.create-form {
  background: #fff;
  padding: 24px;
  border-radius: 14px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.create-form label {
  font-weight: 600;
  color: #333;
}

.create-form input {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-top: 5px;
  font-size: 1em;
}

.create-form span {
  font-size: 0.9em;
  color: #777;
}

.live-summary {
  background: #e9fcef;
  padding: 16px;
  border-radius: 10px;
  font-size: 0.95em;
  color: #004f28;
  line-height: 1.6;
  margin-top: -10px;
}

.create-form button {
  padding: 12px;
  background-color: #17a35e;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.create-form button:hover:enabled {
  background-color: #128f4a;
}

.create-form button:disabled {
  background-color: #ccc;
  color: #666;
  cursor: not-allowed;
}
</style>
