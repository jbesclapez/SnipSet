<template>
  <div class="create-account-page">
    <img src="@/assets/logo.png" alt="Logo" class="logo" />
    <h2>Create Your Account</h2>
    <CreateAccountForm />
    <div class="footer">
      <p>Secure Login with reCAPTCHA subject to Google <a href="https://www.google.com/intl/en/policies/terms">Terms</a> & <a href="https://www.google.com/intl/en/policies/privacy">Privacy</a></p>
    </div>
  </div>
</template>

<script>
import CreateAccountForm from '@/components/CreateAccountForm.vue';

export default {
  name: 'CreateAccount',
  components: {
    CreateAccountForm,
  },
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

.create-account-page {
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

/* Button Styles */
button {
  font-family: var(--main-font-family);
  font-size: 14px; /* Adjust font size to match Login.vue */
  padding: 10px 20px; /* Ensure buttons have the same padding */
  border: none;
  background-color: #000; /* Assuming a primary button color */
  color: white;
  cursor: pointer;
  border-radius: 0;
  transition: background-color 0.3s;
  text-transform: uppercase; /* Make the text uppercase */
  width: 100%;
  max-width: 350px; /* Ensure the width matches the login page */
  text-align: center; /* Center the text */
}

button:hover {
  background-color: #333; /* Darker shade for hover state */
}
</style>
