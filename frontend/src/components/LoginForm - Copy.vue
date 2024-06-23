<template>
  <div class="login-page">
    <img src="@/assets/logo.png" alt="Logo" class="logo" />
    <h2>Log into SnipSet</h2>
    <div class="login-container">
      <div class="login-form-container">
        <form @submit.prevent="login">
          <div class="input-group">
            <label for="email">EMAIL ADDRESS</label>
            <input type="email" id="email" v-model="email" placeholder="name@example.com" required />
            <div class="input-underline"></div>
          </div>
          <div class="input-group password-group">
            <label for="password">PASSWORD</label>
            <div class="password-input-container">
              <input :type="passwordFieldType" id="password" v-model="password" placeholder="Password" required />
              <span class="toggle-password" @click="togglePasswordVisibility">
                <img :src="passwordFieldType === 'password' ? require('@/assets/eye-icon.png') : require('@/assets/eye-slash-icon.png')" alt="Toggle Password Visibility" />
              </span>
            </div>
            <div class="input-underline"></div>
          </div>
          <!-- reCAPTCHA placeholder -->
          <div class="recaptcha-container">
            <VueReCaptcha @verify="onVerify" />
          </div>
          <button :disabled="!isEmailAndPasswordFilled" type="submit" class="login-button">LOG IN</button>
        </form>
      </div>
      <div class="divider-container">
        <div class="divider-line"></div>
        <div class="or-text">OR</div>
        <div class="divider-line"></div>
      </div>
      <div class="social-login-container">
        <button class="social-login-button microsoft-button">
          <img src="@/assets/microsoft-logo.png" alt="Microsoft" class="social-icon" />
          <span>Continue with Microsoft</span>
        </button>
        <button class="social-login-button google-button">
          <img src="@/assets/google-logo.png" alt="Google" class="social-icon" />
          <span>Continue with Google</span>
        </button>
        <button class="social-login-button apple-button">
          <img src="@/assets/apple-logo.png" alt="Apple" class="social-icon" />
          <span>Continue with Apple</span>
        </button>
        <button class="social-login-button facebook-button">
          <img src="@/assets/facebook-logo.png" alt="Facebook" class="social-icon" />
          <span>Continue with Facebook</span>
        </button>
        <button class="create-account-button">CREATE ACCOUNT</button>
      </div>
    </div>
    <a href="#" class="forgot-password">CAN'T LOG IN?</a>
    <div class="footer">
      <p>Secure Login with reCAPTCHA subject to Google <a href="https://www.google.com/intl/en/policies/terms">Terms</a> & <a href="https://www.google.com/intl/en/policies/privacy">Privacy</a></p>
    </div>
  </div>
</template>

<script>
import { VueReCaptcha } from 'vue-recaptcha-v3';

export default {
  components: {
    VueReCaptcha,
  },
  data() {
    return {
      email: '',
      password: '',
      recaptchaVerified: false,
      passwordFieldType: 'password',
    };
  },
  computed: {
    isEmailAndPasswordFilled() {
      return this.email && this.password;
    }
  },
  methods: {
    login() {
      if (this.recaptchaVerified) {
        // Implement your login logic here
      } else {
        alert('Please complete the reCAPTCHA verification.');
      }
    },
    onVerify(token) {
      this.recaptchaVerified = true;
      console.log('reCAPTCHA token:', token); // Optional: Handle token if needed
    },
    togglePasswordVisibility() {
      this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
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

.login-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #fff;
  font-family: var(--main-font-family);
}
.logo {
  width: 50px;
  margin-bottom: 20px;
}
h2 {
  margin-bottom: 20px;
}
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0;
  background: #fff;
  padding: 40px;
  width: 80%; /* Adjust as needed */
  max-width: 800px;
}
.login-form-container {
  flex: 1;
  text-align: left;
  padding-right: 20px;
}
.input-group {
  margin-bottom: 20px;
  position: relative;
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
.password-input-container {
  display: flex;
  align-items: center;
  width: 100%;
}
.password-input-container input {
  flex: 1;
}
.toggle-password {
  cursor: pointer;
  margin-left: 10px;
}
.toggle-password img {
  width: 20px;
  height: 20px;
}
.recaptcha-container {
  margin-bottom: 20px;
}
.login-button, .create-account-button {
  width: 100%;
  padding: 15px;  /* Adjusted height to match social buttons */
  background-color: #e0e0e0; /* Default to disabled color */
  color: white;
  border: none;
  border-radius: 0;
  cursor: pointer;
  margin-top: 10px;
  text-transform: uppercase;
  font-weight: bold;
  font-size: 14px; /* Ensure consistent font size */
  transition: background-color 0.3s ease;
}
.login-button:enabled, .create-account-button:enabled {
  background-color: #000;
}
.login-button:disabled, .create-account-button:disabled {
  cursor: not-allowed;
}
.divider-container {
  display: flex;
  align-items: center;
  flex-direction: column;
  padding: 0 20px;
}
.divider-line {
  width: 1px;
  height: 100px;
  background-color: #ccc;
  margin: 10px 0;
}
.or-text {
  margin: 10px 0;
  color: #666;
  font-size: 14px;
}
.social-login-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.social-login-button {
  width: 100%;
  max-width: 350px;
  padding: 15px;  /* Adjusted height */
  border: 1px solid #ccc;
  border-radius: 0;
  cursor: pointer;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  font-size: 14px;  /* Set font size to 14px */
  background-color: #fff;
  color: #333;  /* Set color to dark grey */
  position: relative;
  overflow: hidden; /* Ensure pseudo-element is contained */
  transition: background-color 0.3s ease; /* Smooth transition for background color */
}
.social-login-button span {
  z-index: 1; /* Ensure text is above pseudo-element */
}
.social-login-button img.social-icon {
  z-index: 1; /* Ensure icon is above pseudo-element */
  width: 20px;
  height: 20px;
  margin-right: 15px;
}
.social-login-button::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.1); /* Adjust the grey color */
  transition: left 0.5s ease; /* Adjust the timing as needed */
}
.social-login-button:hover::before {
  left: 0;
}
.forgot-password {
  display: block;
  margin-top: 20px;
  color: #666;
  text-decoration: none;
  text-align: center;
  text-transform: uppercase;
}
.forgot-password:hover {
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
