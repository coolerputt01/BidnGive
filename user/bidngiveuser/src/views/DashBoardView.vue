<script setup>
import { ref, onMounted , onUnmounted } from 'vue';
import axios from 'axios';

const username = ref('');
const wallet = ref(0);
const bids = ref(0);
const countdown = ref('');
const marketStatus = ref('closed');
const nextAuctionTime = ref('');

const walletUrl = "http://127.0.0.1:8000/api/wallet/balance";
const bidsUrl = "http://127.0.0.1:8000/api/bids/";
const auctionUrl = "http://127.0.0.1:8000/api/admin/auction/status/";

let intervalId = null;

async function fetchAuctionData() {
  try {
    const res = await axios.get(auctionUrl);
    const seconds = res.data.remaining_seconds;
    marketStatus.value = res.data.market_status;
    nextAuctionTime.value = res.data.next_auction;
    startCountdown(seconds);
  } catch (err) {
    console.error("Failed to fetch auction status", err);
  }
}

function startCountdown(initialSeconds) {
  let remaining = initialSeconds;

  clearInterval(intervalId);

  intervalId = setInterval(() => {
    if (remaining <= 0) {
      clearInterval(intervalId);
      fetchAuctionData(); // Re-fetch on expiration
      return;
    }
    const hrs = Math.floor(remaining / 3600);
    const mins = Math.floor((remaining % 3600) / 60);
    const secs = remaining % 60;
    countdown.value = `${hrs}h :${mins}m :${secs}s`;
    remaining -= 1;
  }, 1000);
}

onMounted(async () => {
  const storedUser = localStorage.getItem("userInfo");
  const token = localStorage.getItem("access_token");

  if (storedUser) {
    try {
      const userObj = JSON.parse(storedUser);
      username.value = userObj.username || '';
    } catch (e) {
      console.error("Invalid userInfo in localStorage");
    }
  }

  const headers = {
    Authorization: `Bearer ${token}`
  };

  try {
    const walletResponse = await axios.get(walletUrl, { headers });
    wallet.value = walletResponse.data.balance;
  } catch (error) {
    console.error("Failed to fetch wallet balance", error);
  }

  try {
    const bidsResponse = await axios.get(bidsUrl, { headers });
    bids.value = Array.isArray(bidsResponse.data) ? bidsResponse.data.length : 0;
  } catch (error) {
    console.error("Failed to fetch bids", error);
  }

  await fetchAuctionData(); // initialize countdown
});

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>
<template>
    <main style="background-color: #ebebd3ff;">
        <section style="margin-bottom: 12%;">
            <div style="display: flex;justify-content: space-between;align-items: center;padding: 24px;">
                <div style="line-height: 8px;">
                    <h2 style="font-size: 1.2em;font-weight: 600;">Hello, {{ username }}!</h2>
                    <p style="font-size: 0.9em;">Welcome back</p>
                </div>
                <div>
                    <img src="/icons/notification-on.svg" alt="Notifications Icon" style="width: 1.8em;height: 1.8em;">
                </div>
            </div>
            <section style="display: flex;justify-content: center;align-items: center;flex-direction: column;">
                <div style="text-align: center;display: flex;justify-content: center;align-items: center;border-radius: 3px;">
                    <span style="color: #004f28;background-color: #e0ffe0;font-size: 0.9em;padding: 4px;font-weight: 600;border-radius: 6px;">⏰ Next auction starts in {{ countdown }}</span>
                </div>
                <div style="margin-top: 4%;border-radius: 3px;background-color: #95190C;padding: 12px;width: 80%;">
                    <div>
                        <div style="display: flex;justify-content: space-between;align-items: center;width: 100%;color: #fff;"><p style="font-size: 1.3em;color: #fff;display: flex;justify-content: flex-start;align-items: center;gap: 3%;">Market Status</p> <span style="background-color: #191919;border-radius: 50px;color: #fff;padding: 5px;font-size: 0.9em;padding-left: 10px;padding-right: 10px;">Market {{ marketStatus }}</span></div>
                        <div style="display: flex;justify-content: space-between;align-items: center;width: 100%;color: #fff;"><p>🕐 Next Auction: {{ nextAuctionTime }}</p><p>{{ countdown }}</p></div>
                        <div style="display: flex;justify-content: center;align-items: center;width: 100%;">
                            <button v-if="marketStatus === 'closed'" style="width: 60vw;padding: 10px;background-color: #fff;font-weight: 550;text-align: center;border-radius: 50px;outline: none;border: none;">Auction Closed</button>
                            <button v-else style="width: 60vw;padding: 10px;background-color: #fff;font-weight: 550;text-align: center;border-radius: 50px;outline: none;border: none;">Auction</button>
                        </div>
                    </div>
                </div>

                <!-- Ongoing Bids Card -->
                <div style="margin-top: 4%; border-radius: 12px; background-color: #191919; padding: 20px; width: 80%; max-width: 600px; margin-inline: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <p style="font-size: 1.2em; color: #fff; font-weight: 600; margin-bottom: 10px;">
                    <img src="/icons/moneybag.svg" alt="Bid Icon" style="width: 1.3em; height: 1.3em; margin-right: 6px;" />
                    Ongoing Bids
                </p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #fff; font-size: 1.5em; font-weight: bold;">{{ bids }}</span>
                    <button style="padding: 10px 20px; background-color: #fff; color: #191919; font-weight: 600; border-radius: 50px; border: none; cursor: pointer;">
                    View Bid
                    </button>
                </div>
                </div>
                <!-- Combined Referral Overview -->
<div style="margin-top: 4%; border-radius: 12px; background-color: #e0ffe0; padding: 20px; width: 80%; max-width: 600px; margin-inline: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
  <p style="font-size: 1.2em; color: #004f28; font-weight: 600; margin-bottom: 16px;">🎁 Referral + Daily Bonus</p>
  
  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
    
    <!-- Referral Balance -->
    <div style="flex: 1; min-width: 120px;">
      <p style="color: #004f28; font-size: 0.9em; margin-bottom: 4px;">Bonus</p>
      <span style="font-size: 1.5em; font-weight: bold; color: #004f28;">₦{{ wallet }}</span>
    </div>

    <!-- Withdraw Button -->
    <div style="flex: 1 1 100%; text-align: right;">
      <button style="padding: 10px 20px; background-color: #17a35e; color: #fff; font-weight: 600; border-radius: 50px; border: none; cursor: pointer;">
        Withdraw
      </button>
    </div>
  </div>
</div>
                <!-- Referral Info Card -->
                <div style="margin-top: 4%; border-radius: 12px; background-color: #fff; padding: 20px; width: 80%; max-width: 600px; margin-inline: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <p style="font-size: 1.2em; color: #17a35e; font-weight: 600; margin-bottom: 10px;">📢 Invite & Earn</p>
                <p style="color: #444; font-size: 0.95em; margin-bottom: 10px;">
                    Share your referral code and earn ₦500 for every user that joins and makes a bid.
                </p>
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <input type="text" readonly value="REFCOO" style="flex: 1; min-width: 200px; padding: 10px; border-radius: 6px; border: 1px solid #ccc;" />
                    <button style="padding: 10px 16px; background-color: #17a35e; color: #fff; font-weight: 600; border: none; border-radius: 6px; cursor: pointer;">
                    Copy Code
                    </button>
                </div>
                </div>
            </section>
            <section style="margin-top: 2%;padding: 13px;">
                <section style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 20px; margin-top: 1%; overflow-x: hidden; padding: 10px;">
                    <span class="contact" style="width: auto; height: auto; padding: 20px; border-radius: 50%; background-color: #191919;position: fixed;right: 4%;bottom: 23%;display: flex; align-items: center; justify-content: center;box-shadow: 9px 4px 5px 0px rgba(0,0,0,0.3);">
                        <img src="/icons/whatsapp.svg" alt="Bid icon" style="width: 2em;height: 2em;">
                    </span>
                </section>
            </section>
            <section style="margin-top: 2%;padding: 23px;background-color: #fff;border-radius: 20px;">
                <div style="display: flex;justify-content: space-between;align-items: center;">
                    <div>
                        <span style="color: #191919ff;font-size: 1.3em;font-weight: 600;padding: 5px;">Recent Transactions</span>
                    </div>
                    <div>
                        <span style="color: #191919ff;font-size: 0.9em;font-weight: 600;padding: 5px;color: #172A3A;">View all</span>
                    </div>
                </div>
                <section style="display: flex;justify-content: flex-start;align-items: center;flex-direction: column;margin-top:3%;overflow-x: hidden;">
                    <div style="display: flex;justify-content: space-between;align-items: center;flex-direction: row;border-bottom: 1.2px solid #191919ff;padding: 18px;gap: 5%;">
                        <img src="/icons/credit.svg" alt="Credit alert" style="width: 1.8em;height: 1.8em;background-color: lightgrey;border-radius: 50%;padding: 12px;">
                        <span style="line-height: 6px;width: 60vw;">
                            <span style="font-size: 1.3em;font-weight: 600;width: 100%;">Mr Adeniyi Samuel</span>
                            <p style="font-size: 1em;font-weight: normal;width: 100%;color: grey">Recommitment</p>
                        </span>
                        <span style="font-size: 1.3em;font-weight: 600;">
                            &#8358;5,000
                        </span>
                    </div>
                    <div style="display: flex;justify-content: space-between;align-items: center;flex-direction: row;border-bottom: 1.2px solid #191919ff;padding: 18px;gap: 5%;">
                        <img src="/icons/credit.svg" alt="Credit alert" style="width: 1.8em;height: 1.8em;background-color: lightgrey;border-radius: 50%;padding: 12px;">
                        <span style="line-height: 6px;width: 60vw;">
                            <span style="font-size: 1.3em;font-weight: 600;width: 100%;">Mr Adeniyi Samuel</span>
                            <p style="font-size: 1em;font-weight: normal;width: 100%;color: grey">Recommitment</p>
                        </span>
                        <span style="font-size: 1.3em;font-weight: 600;">
                            &#8358;5,000
                        </span>
                    </div>
                </section>
            </section>
        </section>
        <NavBar />
    </main>
</template>