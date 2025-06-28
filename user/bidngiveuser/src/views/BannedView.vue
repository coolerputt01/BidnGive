<template>
  <main class="banned-page">
    <section class="card">
      <img src="/icons/blocked.svg" alt="Blocked" class="icon" />
      <h2>You’ve Been Banned</h2>
      <p>Your account has been temporarily suspended due to policy violations or unconfirmed payments.</p>
      <p class="note">Please contact support if you believe this was a mistake.</p>

      <a href="https://wa.me/2348000000000" class="btn">📞 Contact Support</a>
    </section>
  </main>
</template>

<script setup>
// No script needed unless you want to auto-logout or redirect later.
</script>

<style scoped>
.banned-page {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f7f9f9;
  height: 100vh;
  padding: 20px;
  font-family: 'Segoe UI', sans-serif;
}

.card {
  background: #fff;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  max-width: 500px;
  text-align: center;
}

.icon {
  width: 80px;
  margin-bottom: 20px;
}

h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #dc3545;
  margin-bottom: 10px;
}

p {
  color: #444;
  font-size: 0.95rem;
  margin-bottom: 10px;
}

.note {
  font-size: 0.85rem;
  color: #666;
}

.btn {
  margin-top: 20px;
  display: inline-block;
  background-color: #17a35e;
  color: #fff;
  padding: 12px 24px;
  border-radius: 30px;
  text-decoration: none;
  font-weight: 600;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #128f4a;
}
</style>
