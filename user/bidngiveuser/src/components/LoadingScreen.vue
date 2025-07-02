<template>
  <div class="loading-screen">
    <div class="loader-content">
      <img src="/logo.png" alt="Logo" class="logo" />
      <div class="spinner"></div>
      <p class="message">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: 'Loading, please wait...'
  }
})
</script>

<style scoped>
.loading-screen {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.3s ease-in-out;
}

.loader-content {
  text-align: center;
}

.logo {
  width: 60px;
  height: 60px;
  margin-bottom: 20px;
  animation: pulse 1.5s infinite ease-in-out;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 15px;
  border: 4px solid #17a35e;
  border-top: 4px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.message {
  font-size: 1em;
  font-weight: 500;
  color: #444;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.9;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
