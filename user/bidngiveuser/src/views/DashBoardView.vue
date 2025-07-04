<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { toast } from 'vue3-toastify';
import axios from 'axios';
import LoadingScreen from '@/components/LoadingScreen.vue';

const username = ref('');
const canJoinAuction = ref(true);
const wallet = ref(0);
const bids = ref(0);
const countdown = ref('');
const marketStatus = ref('closed');
const nextAuctionTime = ref('');
const referralCode = ref('');
const isAuctionRoom = ref(false);
const joiningAuction = ref(false);
const hasMergedBid = ref(false);
const withdrawingReferral = ref(false);
const loading = ref(true);

const baseUrl = "https://bidngive.com/signup";
const router = useRouter();

const walletUrl = "https://bidngive.onrender.com/api/wallet/balance";
const bidsUrl = "https://bidngive.onrender.com/api/bids/";
const auctionUrl = "https://bidngive.onrender.com/api/admin/auction/status/";
const userUrl = "https://bidngive.onrender.com/api/accounts/me/";

const hasClickedJoin = ref(false);


let intervalId = null;

function copyCode() {
  const link = `${baseUrl}?ref=${referralCode.value}`;
  navigator.clipboard.writeText(link).then(() => {
    toast.success("Referral link copied!");
  });
}

function startCountdown(initialSeconds) {
  let remaining = initialSeconds;
  clearInterval(intervalId);

  intervalId = setInterval(() => {
    if (remaining <= 0) {
      clearInterval(intervalId);
      canJoinAuction.value = false;
      fetchAuctionData();
      return;
    }

    const hrs = Math.floor(remaining / 3600);
    const mins = Math.floor((remaining % 3600) / 60);
    const secs = remaining % 60;
    countdown.value = `${hrs}h :${String(mins).padStart(2, '0')}m :${String(secs).padStart(2, '0')}s`;

    remaining -= 1;
  }, 1000);
}


async function fetchAuctionData() {
  try {
    const res = await axios.get(auctionUrl);
    const seconds = res.data.remaining_seconds;
    marketStatus.value = res.data.market_status;
    nextAuctionTime.value = new Date(Date.now() + seconds * 1000).toISOString(); // derive from now

    canJoinAuction.value = res.data.market_status === 'open';
    if (res.data.market_status === 'closed') {
        hasClickedJoin.value = false;
      }

    clearInterval(intervalId);
    startCountdown(seconds);
  } catch (err) {
    console.error("Failed to fetch auction status", err);
  }
}

const tryClaimDailyBonus = async () => {
  const token = localStorage.getItem('access_token');
  const lastBonusDate = localStorage.getItem('last_bonus_date');
  const today = new Date().toISOString().split('T')[0];

  if (lastBonusDate === today) return;

  try {
    const res = await axios.post('https://bidngive.onrender.com/api/wallet/daily-bonus/', {}, {
      headers: { Authorization: `Bearer ${token}` }
    });

    toast.success(res.data.message + ` 🎁 ₦100! New Balance: ₦${res.data.balance.toLocaleString()}`);
    localStorage.setItem('last_bonus_date', today);
  } catch (err) {
    if (err.response?.data?.message === "Already claimed today") {
      localStorage.setItem('last_bonus_date', today);
    }
  }
};

async function joinAuctionRoom() {
  const token = localStorage.getItem("access_token");
  const headers = { Authorization: `Bearer ${token}` };

  if (isAuctionRoom.value) {
    toast.info("You've already joined the auction room.");
    return;
  }

  joiningAuction.value = true;
  hasClickedJoin.value = true;
  try {
    await axios.patch(userUrl, { is_auction_room: true }, { headers });
    isAuctionRoom.value = true;
    toast.success("✅ You have successfully joined the auction room.");
  } catch (err) {
    hasClickedJoin.value = false;
    console.error("Failed to join auction room", err);
    toast.error("Failed to join auction room.");
  } finally {
    joiningAuction.value = false;
  }
}

function formatAuctionTime(isoString) {
  try {
    const utcDate = new Date(isoString);
    const options = {
      timeZone: 'Africa/Lagos',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    };
    return new Intl.DateTimeFormat('en-NG', options).format(utcDate);
  } catch {
    return 'Invalid time';
  }
}


async function withdrawReferral() {
  if (withdrawingReferral.value) return;

  if (wallet.value < 10000) {
    toast.warning("🚫 You need at least ₦10,000 referral bonus to withdraw.");
    return;
  }

  if (wallet.value > 500000) {
    toast.warning("🚫 Maximum withdrawal is ₦500,000 at a time.");
    return;
  }

  const token = localStorage.getItem("access_token");
  const headers = { Authorization: `Bearer ${token}` };

  withdrawingReferral.value = true;

  try {
    await axios.post(
      "https://bidngive.onrender.com/api/bids/",
      {
        amount: wallet.value,
        type: "referral_withdraw",
        plan: "referral_mode"
      },
      { headers }
    );

    toast.success("🎉 Referral withdrawal bid created!");
    router.push("/bid");
  } catch (error) {
    console.error("Referral withdrawal failed:", error);
    toast.error("Failed to create referral withdrawal bid.");
  } finally {
    withdrawingReferral.value = false;
  }
}

function viewBid() {
  router.push('/create-bid');
}

onMounted(async () => {
  loading.value = true;
  const token = localStorage.getItem("access_token");
  const headers = { Authorization: `Bearer ${token}` };

  try {
    tryClaimDailyBonus();

    try {
      const userRes = await axios.get(userUrl, { headers });
      username.value = userRes.data.username || '';
      referralCode.value = userRes.data.referral_code || '';
      isAuctionRoom.value = userRes.data.is_auction_room;
    } catch (err) {
      console.error("User fetch failed", err);
    }

    try {
      const walletResponse = await axios.get(walletUrl, { headers });
      wallet.value = walletResponse.data.balance;
    } catch (error) {
      console.error("Failed to fetch wallet balance", error);
    }

    try {
      const bidsResponse = await axios.get(bidsUrl, { headers });
      const userBids = Array.isArray(bidsResponse.data) ? bidsResponse.data : [];
      bids.value = userBids.length;

      hasMergedBid.value = userBids.some(bid => bid.status === 'merged');
      if (hasMergedBid.value) {
        toast.info("📦 You have a pending merged bid! Please check and upload payment proof.", {
          position: "top-right",
          autoClose: false,
        });
      }
    } catch (error) {
      console.error("Failed to fetch bids", error);
    }

    await fetchAuctionData();
    console.log(nextAuctionTime)
  } finally {
    loading.value = false;
  }
});

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>

<template>
  <main v-if="!loading" style="background-color: #ebebd3ff;padding-bottom: 5em;">
    <section style="margin-bottom: 12%;">
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 24px;">
        <div style="line-height: 8px;">
          <h2 style="font-size: 1.2em; font-weight: 600;">Hello, {{ username }}!</h2>
          <p style="font-size: 0.9em;">Welcome back</p>
        </div>
        <img src="/icons/refer.png" alt="Notifications Icon" style="width: 1.8em; height: 1.8em;mix-blend-mode:multiply;cursor: pointer;" @click="router.push('/referrals')">
      </div>

      <section style="display: flex; flex-direction: column; align-items: center;">
        <span style="color: #004f28; background-color: #e0ffe0; font-size: 0.9em; padding: 4px 8px; font-weight: 600; border-radius: 6px;">
          ⏰ Next auction starts in {{ countdown }}
        </span>

        <div style="margin-top: 4%; background-color: #95190C; padding: 12px; width: 80%; border-radius: 12px;">
          <div style="color: #fff; display: flex; justify-content: space-between; margin-bottom: 10px;">
            <p style="font-size: 1.3em;">Market Status</p>
            <span style="background-color: #000; display: flex; justify-content: center; padding: 1%; align-items: center; color: #fff; font-weight: 500; border-radius: 50px;">
              Market {{ marketStatus }}
            </span>
          </div>
          <div style="color: #fff; display: flex; justify-content: space-between;">
            <p>🕐 Next Auction: {{ formatAuctionTime(nextAuctionTime) }}</p>
            <p>{{ countdown }}</p>
          </div>

          <div style="margin-top: 12px; text-align: center;">
            <button
    v-if="marketStatus === 'open'"
    :disabled="joiningAuction || hasClickedJoin"
    @click="joinAuctionRoom"
    style="width: 60vw; padding: 10px; background-color: #fff; font-weight: 600; border-radius: 50px; border: none; cursor: pointer;"
  >
    {{
      joiningAuction
        ? 'Joining...'
        : hasClickedJoin
          ? 'Already Clicked'
          : 'Join Auction Room'
    }}
  </button>



            <p v-else-if="marketStatus === 'open' && hasClickedJoin" style="color: #e0ffe0; font-size: 0.95em; margin-top: 10px;">
              ✅ You are in the Auction Room
            </p>

            <button
              v-else
              disabled
              style="width: 60vw; padding: 10px; background-color: #ccc; font-weight: 600; border-radius: 50px; border: none;"
            >
              Auction Closed
            </button>
          </div>
        </div>

        <div style="margin-top: 4%; background-color: #191919; padding: 20px; width: 80%; border-radius: 12px;">
          <p style="color: #fff; font-size: 1.2em; font-weight: 600;">
            <img src="/icons/moneybag.svg" style="width: 1.3em; margin-right: 6px;" /> Ongoing Bids
          </p>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
            <span style="color: #fff; font-size: 1.5em; font-weight: bold;">{{ bids }}</span>
            <button @click="viewBid" style="padding: 10px 20px; background-color: #fff; color: #191919; font-weight: 600; border-radius: 50px; border: none; cursor: pointer;">
              Create Bid
            </button>
          </div>
        </div>

        <div style="margin-top: 4%; background-color: #e0ffe0; padding: 20px; width: 80%; border-radius: 12px;">
          <p style="font-size: 1.2em; color: #004f28; font-weight: 600;">🎁 Referral + Daily Bonus</p>
          <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
            <div>
              <p style="color: #004f28; font-size: 0.9em;">Bonus</p>
              <span style="font-size: 1.5em; font-weight: bold;">₦{{ wallet ? wallet.toLocaleString() : '0.00' }}</span>
            </div>
            <button @click="withdrawReferral" style="background-color: #17a35e; color: #fff; font-weight: 600; border-radius: 50px; border: none; display: flex; justify-content: center; padding: 1.3%; align-items: center;">
              Withdraw
            </button>
          </div>
        </div>

        <div style="margin-top: 4%; background-color: #fff; padding: 20px; width: 80%; border-radius: 12px;">
          <p style="font-size: 1.2em; color: #17a35e; font-weight: 600;">📢 Invite & Earn</p>
          <div style="color: #444; font-size: 0.95em; line-height: 1.6;">
              <p>₦100 Daily Bonus</p>
              <p>5% referral bonus</p>
            </div>

          <div style="display: flex; gap: 10px; margin-top: 10px;">
            <input readonly :value="`${baseUrl}?ref=${referralCode}`" style="flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 6px;" />
            <button @click="copyCode" style="padding: 10px 16px; background-color: #17a35e; color: #fff; font-weight: 600; border-radius: 6px; cursor: pointer;">
              Copy Link
            </button>
          </div>
          <!-- WhatsApp Support Button -->
          <a
            href="https://chat.whatsapp.com/FYJIaAqY3tw9OTuASmMjBB?mode=r_t" 
            target="_blank"
            class="whatsapp-support"
            aria-label="Chat on WhatsApp"
          >
            <img src="/icons/whatsapp.svg" alt="WhatsApp Support" />
          </a>

        </div>
      </section>
    </section>
  </main>
  <!-- Loading Screen -->
  <main v-else>
    <LoadingScreen message="Fetching your dashboard..." />
  </main>
</template>

<style>
.whatsapp-support {
  position: fixed;
  bottom: 120px;
  right: 16px;
  z-index: 9999;
  padding: 10px;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease;
}

.whatsapp-support:hover {
  transform: scale(1.1);
}

.whatsapp-support img {
  width: 32px;
  height: 32px;
}
</style>
