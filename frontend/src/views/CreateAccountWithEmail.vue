<template>
  <div class="create-account-email-page">
    <img src="@/assets/logo.png" alt="Logo" class="logo" />
    <h2>Create Your Account</h2>
    <form @submit.prevent="createAccount">
      <div class="input-group">
        <label for="firstname">FIRST NAME</label>
        <input type="text" id="firstname" v-model="firstname" placeholder="First Name" required />
        <div class="input-underline"></div>
      </div>
      <div class="input-group">
        <label for="lastname">LAST NAME</label>
        <input type="text" id="lastname" v-model="lastname" placeholder="Last Name" required />
        <div class="input-underline"></div>
      </div>
      <div class="input-group">
        <label for="email">EMAIL ADDRESS</label>
        <input type="email" id="email" v-model="email" placeholder="name@example.com" required />
        <div class="input-underline"></div>
      </div>
      <div class="input-group">
        <label for="password">PASSWORD</label>
        <input type="password" id="password" v-model="password" placeholder="Password" required />
        <div class="input-underline"></div>
      </div>
      <p class="terms-text">
        By creating an account, you agree to our <a href="#">Terms of Service</a> and have read and understood the <a href="#">Privacy Policy</a>
      </p>
      <button :disabled="!isFormFilled" type="submit" class="create-account-button">Continue</button>
    </form>
    <a @click.prevent="goBack" href="#" class="back-button">Back</a>
    <div class="footer">
      <p>Secure Login with reCAPTCHA subject to Google <a href="https://www.google.com/intl/en/policies/terms">Terms</a> & <a href="https://www.google.com/intl/en/policies/privacy">Privacy</a></p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CreateAccountWithEmail',
  data() {
    return {
      firstname: '',
      lastname: '',
      email: '',
      password: ''
    };
  },
  computed: {
    isFormFilled() {
      return this.firstname && this.lastname && this.email && this.password;
    }
  },
  methods: {
    async createAccount() {
      try {
        const response = await axios.post('http://localhost:5000/api/auth/signup', {
          username: this.email,
          email: this.email,
          password: this.password,
          name: this.lastname,
          firstname: this.firstname
        });
        if (response.status === 201 || response.data.message === "Account created") {
          // Handle successful account creation (e.g., redirect to login page)
          this.$router.push('/login');
        } else {
          // Handle unexpected responses
          console.error('Account creation failed:', response.data);
        }
      } catch (error) {
        console.error('Account creation error:', error);
      }
    },
    goBack() {
      this.$router.push('/create-account');
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

.create-account-email-page {
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
.terms-text {
  margin-bottom: 20px;
  font-size: 12px;
  color: grey;
  text-align: center;
}
.terms-text a {
  color: grey;
  text-decoration: underline;
}
.create-account-button {
  width: 100%;
  padding: 15px;
  background-color: #e0e0e0;
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
.create-account-button:enabled {
  background-color: #000;
}
.create-account-button:disabled {
  cursor: not-allowed;
}
.back-button {
  display: block;
  margin-top: 20px;
  color: #666;
  text-decoration: none;
  text-align: center;
  text-transform: uppercase;
}
.back-button:hover {
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
