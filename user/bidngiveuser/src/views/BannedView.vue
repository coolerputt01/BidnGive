<template>
  <main class="banned-hero">
    <section class="banned-content">
      <img src="/icons/blocked.svg" alt="Blocked Icon" class="blocked-icon" />

      <h1 class="banned-title">Access Restricted</h1>
      <p class="banned-text">
        Your BID ‘N’ GIVE account has been <strong>suspended</strong> due to unresolved issues —
        either unconfirmed payments or policy violations.
      </p>

      <p class="banned-subtext">
        If this was a mistake, you can reach out immediately to resolve it.
      </p>

      <a href="https://wa.me/2348000000000" class="contact-btn pulse">
        📞 Contact Support via WhatsApp
      </a>
    </section>

    <div class="banned-bg-layer"></div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue';

onMounted(() => {
  console.log('🚫 User blocked page mounted');
});
</script>

<style scoped>
.banned-hero {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(to bottom, #ffecec 0%, #fff 100%);
  overflow: hidden;
  position: relative;
  padding: 20px;
  text-align: center;
  font-family: 'Segoe UI', sans-serif;
}

.banned-bg-layer {
  position: absolute;
  background: url('/images/banned-bg.svg') no-repeat center;
  background-size: cover;
  opacity: 0.07;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1;
  pointer-events: none;
}

.banned-content {
  z-index: 2;
  max-width: 720px;
  width: 100%;
  color: #222;
}

.blocked-icon {
  width: 100px;
  margin-bottom: 1rem;
  animation: float 3s ease-in-out infinite;
}

.banned-title {
  font-size: 2.4rem;
  font-weight: 800;
  color: #b00020;
  margin-bottom: 1rem;
}

.banned-text {
  font-size: 1.05rem;
  line-height: 1.6;
  margin-bottom: 0.8rem;
  color: #444;
}

.banned-subtext {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 2rem;
}

.contact-btn {
  background-color: #17a35e;
  color: #fff;
  padding: 14px 28px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 50px;
  text-decoration: none;
  display: inline-block;
  transition: background-color 0.3s ease;
}

.contact-btn:hover {
  background-color: #128f4a;
}

/* Pulse animation */
.pulse {
  animation: pulseAnim 2s infinite;
}

@keyframes pulseAnim {
  0% {
    box-shadow: 0 0 0 0 rgba(23, 163, 94, 0.5);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(23, 163, 94, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(23, 163, 94, 0);
  }
}

/* Icon float */
@keyframes float {
  0% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
  100% { transform: translateY(0); }
}
</style>
