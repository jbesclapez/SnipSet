<template>
  <div class="forgot-password-page">
    <img src="@/assets/logo.png" alt="Logo" class="logo" />
    <h2>Forgot Password</h2>
    <p>Enter your account’s email and we’ll send you an email to reset the password.</p>
    <div class="forgot-password-container">
      <form @submit.prevent="sendEmail">
        <div class="input-group">
          <label for="email">EMAIL ADDRESS</label>
          <input type="email" id="email" v-model="email" placeholder="name@example.com" required />
          <div class="input-underline"></div>
        </div>
        <button :disabled="!email" type="submit" class="send-email-button">SEND EMAIL</button>
      </form>
      <a @click="goToForgotEmail" class="forgot-email-link">FORGOT THE EMAIL ADDRESS?</a>
    </div>
    <div class="footer">
      <p>Secure Login with reCAPTCHA subject to Google <a href="https://www.google.com/intl/en/policies/terms">Terms</a> & <a href="https://www.google.com/intl/en/policies/privacy">Privacy</a></p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
    };
  },
  methods: {
    async sendEmail() {
      try {
        const response = await axios.post('http://localhost:5000/api/auth/forgot-password', {
          email: this.email,
        });
        if (response.data.message === "Email sent") {
          alert('A reset link has been sent to your email.');
          this.$router.push('/login');
        } else {
          alert('An error occurred. Please try again.');
        }
      } catch (error) {
        console.error('Error sending email:', error);
        alert('An error occurred. Please try again.');
      }
    },
    goToForgotEmail() {
      this.$router.push('/forgot-email');
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Roboto:400,500&display=swap');

:root {
  --main-font-family: 'Roboto', sans-serif;
}

body {
  font-family: var(--main-font-family);
}

.forgot-password-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #fff;
  font-family: var(--main-font-family);
  position: relative;
}

.logo {
  width: 50px;
  margin-bottom: 20px;
}

h2 {
  margin-bottom: 20px;
}

p {
  margin-bottom: 20px;
  text-align: center;
  max-width: 400px;
}

.forgot-password-container {
  width: 80%;
  max-width: 400px;
}

.input-group {
  margin-bottom: 20px;
  position: relative;
  width: 100%;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
}

.input-group input {
  width: 100%;
  padding: 10px;
  border: none;
  border-bottom: 1px solid #ccc;
  outline: none;
}

.input-group input:focus + .input-underline {
  background-color: #333;
  height: 2px;
}

.input-underline {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background-color: #ccc;
  transition: background-color 0.3s, height 0.3s;
}

.send-email-button {
  width: 100%;
  padding: 15px;
  background-color: #000;
  color: white;
  border: none;
  border-radius: 0;
  cursor: pointer;
  margin-top: 10px;
  text-transform: uppercase;
  font-weight: bold;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.send-email-button:disabled {
  background-color: #e0e0e0;
  cursor: not-allowed;
}

.forgot-email-link {
  display: block;
  margin-top: 20px;
  color: #666;
  text-decoration: none;
  text-align: center;
  text-transform: uppercase;
}

.forgot-email-link:hover {
  text-decoration: underline;
}

.footer {
  text-align: center;
  margin-top: 20px;
  font-size: 12px;
  color: grey;
}

.footer a {
  color: grey;
  text-decoration: underline;
}
</style>
