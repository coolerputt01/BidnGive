<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <section class="tos-wrapper">
    <button class="back-button" @click="router.go(-1)">← Back</button>

    <div class="tos-container">
      <header class="tos-header">
        <h1>Terms of Service</h1>
        <p class="effective-date">Effective: <span>16th June, 2025</span></p>
      </header>

      <section class="tos-section">
        <h2>1. Introduction</h2>
        <p>
          Welcome to <strong>BID "N" GIVE Ltd</strong>, a platform based in Nigeria that allows individuals, businesses,
          and those in financial need to participate in a simple, money-earning system.
        </p>
        <p>
          By accessing or using our platform, you agree to be legally bound by these Terms of Service.
          Please read them carefully before proceeding.
        </p>
      </section>

      <section class="tos-section">
        <h2>2. Eligibility</h2>
        <p>
          Our services are only available to individuals aged 18 and above. By creating an account, you confirm that you meet
          this requirement and take full responsibility for the use of your account.
        </p>
      </section>

      <section class="tos-section">
        <h2>3. Account Registration</h2>
        <p>
          To use our services, you must create an account using your full name, email address, phone number, and valid Nigerian
          bank details. We do not use OAuth or social login services.
        </p>
        <p class="bg-note">
          <strong>Responsibility:</strong> Keep your login credentials secure. You are responsible for all activity on your account.
        </p>
      </section>

      <section class="tos-section">
        <h2>4. Platform Features</h2>
        <p>
          BID "N" GIVE is a <span class="highlight">completely free</span> platform. We do not offer any paid or premium features.
          All users have access to the same tools and opportunities.
        </p>
      </section>

      <section class="tos-section">
        <h2>5. Permitted Use</h2>
        <p>
          Our platform is meant for legitimate investment activities. Users must not use the service for any kind of scam, fraud,
          or illegal financial manipulation.
        </p>
        <p class="bg-warning">
          ⚠️ <strong>Important:</strong> Fraudulent activity will result in immediate suspension or permanent account ban.
        </p>
      </section>

      <section class="tos-section">
        <h2>6. Data Collection & Privacy</h2>
        <p>
          We only collect essential personal data: your name, email, phone number, and bank account details.
          We do <strong>not</strong> share your data with third-party tools or advertisers.
        </p>
        <p>
          You may request deletion of your data at any time by contacting us.
        </p>
      </section>

      <section class="tos-section">
        <h2>7. Account Deletion</h2>
        <p>
          You have full control of your account and may delete it at any time via your dashboard. Once deleted, your data is permanently removed from our system.
        </p>
      </section>

      <section class="tos-section">
        <h2>8. Updates to the Terms</h2>
        <p>
          We reserve the right to modify or update these Terms at any time. Any significant changes will be posted on this page.
          Your continued use of the platform after changes are published means you accept the revised Terms.
        </p>
      </section>

      <section class="tos-section">
        <h2>9. Contact Us</h2>
        <p>
          If you have any questions or concerns about these Terms of Service, please contact us at:
          <br />
          <span class="highlight">bidngive01@gmail.com</span>
        </p>
      </section>
    </div>
  </section>
</template>

<style scoped>
.tos-wrapper {
  background: #f7f7f5;
  padding: 3rem 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
}

.back-button {
  align-self: flex-start;
  margin-bottom: 1rem;
  margin-left: 1rem;
  background-color: transparent;
  color: #04724d;
  border: 2px solid #04724d;
  border-radius: 999px;
  padding: 0.45rem 1rem;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-button:hover {
  background-color: #04724d;
  color: white;
}

.tos-container {
  max-width: 800px;
  width: 100%;
  padding: 2rem;
  font-family: "Segoe UI", sans-serif;
  background-color: transparent;
  color: #222;
}

.tos-header {
  text-align: center;
  margin-bottom: 2rem;
}

.tos-header h1 {
  font-size: 2.2rem;
  color: #04724d;
  margin-bottom: 0.4rem;
}

.effective-date {
  font-size: 0.95rem;
  color: #555;
}

.effective-date span {
  color: #04724d;
  font-weight: 600;
}

.tos-section {
  margin-bottom: 2.2rem;
}

.tos-section h2 {
  font-size: 1.4rem;
  color: #04724d;
  margin-bottom: 0.6rem;
}

.tos-section p {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #333;
}

.highlight {
  color: #04724d;
  font-weight: 600;
}

.bg-note {
  background-color: #e7f8f2;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  font-size: 0.98rem;
  color: #044f39;
}

.bg-warning {
  background-color: #fff5f5;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  font-size: 0.98rem;
  color: #b71c1c;
}

@media (max-width: 600px) {
  .tos-container {
    padding: 1rem;
  }

  .back-button {
    font-size: 0.85rem;
    margin-left: 0;
  }

  .tos-header h1 {
    font-size: 1.8rem;
  }

  .tos-section h2 {
    font-size: 1.2rem;
  }

  .tos-section p {
    font-size: 1rem;
  }
}
</style>
