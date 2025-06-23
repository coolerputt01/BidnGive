<template>
  <main class="not-found">
    <div class="illustration">
      <img src="/images/notfound.gif" alt="404 Illustration" />
    </div>

    <div class="content">
      <h1>Oops! Page Not Found</h1>
      <p>
        The page you're looking for doesn't exist or has been moved.<br />
        If you think this is a mistake, please contact support.
      </p>

      <router-link to="/login" class="btn">Return to Login</router-link>
    </div>
  </main>
</template>

<script setup>
// No logic needed for static 404 page
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  background-color: #f8f9fa;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  font-family: 'Arial', sans-serif;
  overflow: hidden;
}

.illustration img {
  max-width: 300px;
  margin-bottom: 30px;
  mix-blend-mode: multiply;
}

.content h1 {
  font-size: 2.2em;
  color: #191919;
  margin-bottom: 10px;
}

.content p {
  font-size: 1em;
  color: #555;
  margin-bottom: 25px;
  line-height: 1.5;
}

.btn {
  background-color: #17a35e;
  color: #fff;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  font-size: 1em;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #128f4a;
}
</style>
