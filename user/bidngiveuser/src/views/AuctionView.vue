<template>
  <section class="bids-page">
    <section class="header">
      <h2>Available Bids</h2>
      <p>Choose a bid to join and start earning returns</p>
    </section>

    <div style="text-align: center; display: flex; justify-content: center; align-items: center; border-radius: 3px;">
      <span style="color: #004f28; background-color: #e0ffe0; font-size: 0.9em; padding: 4px; font-weight: 600; border-radius: 6px;">
        ⏰ Next auction starts in 0h :01m :0s
      </span>
    </div>

    <section class="info-banner">
      💡 How it works: Join a bid, pay a partner, and receive returns within the agreed time.
    </section>

    <section class="bids-section">
      <div v-for="(bid, index) in bids" :key="index" class="bid-card">
        <div class="bid-top">
          <span class="bid-amount">₦{{ bid.amount }}</span>
          <span class="bid-return">Return: {{ bid.return }}%</span>
        </div>
        <div class="bid-details">
          <p>Partner: <strong>{{ bid.partner }}</strong></p>
          <p>Duration: {{ bid.duration }} days</p>
        </div>
        <button class="btn-join">Join Bid</button>
      </div>
    </section>
  </section>
</template>

<script setup>
const bids = [
  { amount: 10000, return: 20, duration: 7, partner: "Emeka A." },
  { amount: 5000, return: 15, duration: 5, partner: "Fatima B." },
  { amount: 20000, return: 25, duration: 10, partner: "John O." }
];
</script>

<style scoped>
.bids-page {
  background-color: #f4f4f4;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.header h2 {
  font-size: 1.8em;
  font-weight: 700;
  color: #191919;
}

.header p {
  font-size: 0.95em;
  color: #555;
}

.info-banner {
  background-color: #e0ffe0;
  padding: 12px;
  border-left: 5px solid #17a35e;
  font-size: 0.9em;
  color: #004f28;
  margin: 20px 0;
  border-radius: 6px;
}

.bids-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.bid-card {
  background-color: #fff;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s;
}

.bid-card:hover {
  transform: scale(1.01);
}

.bid-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 1.1em;
}

.bid-amount {
  font-weight: bold;
  color: #17a35e;
}

.bid-return {
  font-weight: bold;
  color: #95190c;
}

.bid-details p {
  margin: 4px 0;
  color: #333;
}

.btn-join {
  margin-top: 12px;
  padding: 10px;
  width: 100%;
  background-color: #17a35e;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-join:hover {
  background-color: #128f4a;
}
</style>
