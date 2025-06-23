<script>
import { useRouter } from "vue-router";

const router = useRouter();
</script>
<template>
  <section class="tos-wrapper">
    <div class="tos-container">
      <header class="tos-header">
        <button class="back-button" @click="router.go(-1)">← Back</button>
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
        <div class="card">
          <strong>Your Responsibility:</strong> Keep your login credentials secure. You are responsible for all activity on your account.
        </div>
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
        <div class="warning">
          ⚠️ <strong>Important:</strong> Fraudulent activity will result in immediate suspension or permanent account ban.
        </div>
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
          <span class="highlight">[Your Contact Placeholder]</span>
        </p>
      </section>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<style scoped>
.tos-wrapper {
  background: #f5f5f5;
  padding: 4rem 1rem;
  display: flex;
  justify-content: center;
}

.tos-container {
  max-width: 840px;
  width: 100%;
  background: #fff;
  padding: 3rem 2rem;
  border-radius: 12px;
  border: 1px solid #eee;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
  color: #222;
}

.tos-header {
  text-align: center;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1.5rem;
  margin-bottom: 2rem;
  position: relative;
}

.back-button {
  position: absolute;
  left: 0;
  top: 0;
  background: #04724dff;
  color: #fff;
  border: none;
  padding: 0.5rem 1.2rem;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.2s;
}

.back-button:hover {
  background: #035c3eff;
}

.tos-header h1 {
  font-size: 2.4rem;
  color: #04724dff;
  margin-bottom: 0.4rem;
}

.effective-date {
  font-size: 0.95rem;
  color: #555;
}

.effective-date span {
  color: #04724dff;
  font-weight: 600;
}

.tos-section {
  margin-bottom: 2.5rem;
}

.tos-section h2 {
  font-size: 1.4rem;
  color: #04724dff;
  margin-bottom: 0.75rem;
}

.tos-section p {
  font-size: 1.05rem;
  line-height: 1.7;
  margin-bottom: 1rem;
}

.highlight {
  color: #04724dff;
  font-weight: 600;
}

.card {
  background: #f0fdf9;
  border-left: 4px solid #04724dff;
  padding: 1rem 1rem;
  border-radius: 6px;
  margin-top: 0.5rem;
  font-size: 0.98rem;
  color: #044233;
}

.warning {
  background: #fff5f5;
  border-left: 4px solid #cc0000;
  padding: 1rem 1rem;
  border-radius: 6px;
  font-size: 0.98rem;
  color: #660000;
  margin-top: 1rem;
}
</style>
