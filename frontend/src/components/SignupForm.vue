<!-- src/components/SignupForm.vue -->
<template>
  <div class="container">
    <div class="form-wrapper">
      <img :src="theme.logoUrl" :alt="theme.companyName" class="logo" />
      <h1 class="title">Sign up for {{ theme.companyName }}</h1>
      <input v-model="username" type="text" placeholder="Username" class="input" />
      <input v-model="email" type="email" placeholder="Email Address" class="input" />
      <input v-model="password" type="password" placeholder="Password" class="input" />
      <input v-model="name" type="text" placeholder="Name" class="input" />
      <input v-model="firstname" type="text" placeholder="Firstname" class="input" />
      <select v-model="securityQuestion" class="input">
        <option value="" disabled>Select a security question</option>
        <option value="question1">What is your pet's name?</option>
        <option value="question2">What is your mother's maiden name?</option>
        <option value="question3">What was your first car?</option>
      </select>
      <input v-model="securityAnswer" type="text" placeholder="Security Answer" class="input" />
      <vue-recaptcha sitekey="YOUR_RECAPTCHA_SITE_KEY" @verify="onCaptchaVerified" />
      <button @click="handleSignup" class="button">Sign Up</button>
    </div>
  </div>
</template>

<script>
import { theme } from '../theme';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      name: '',
      firstname: '',
      securityQuestion: '',
      securityAnswer: '',
      captchaValue: null,
      theme,
    };
  },
  methods: {
    handleSignup() {
      if (!this.captchaValue) {
        alert('Please complete the CAPTCHA');
        return;
      }
      // Implement signup API call here
    },
    onCaptchaVerified(response) {
      this.captchaValue = response;
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
  justify-content: center;
  align-items: center;
  background-color: var(--background-color);
}
.form-wrapper {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 400px;
  text-align: center;
}
.logo {
  height: 50px;
  margin-bottom: 20px;
}
.title {
  color: var(--text-color);
  margin-bottom: 20px;
}
.input {
  width: calc(100% - 20px);
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
}
.button:hover {
  background-color: var(--secondary-color);
}
</style>
