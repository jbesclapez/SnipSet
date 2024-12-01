<template>
  <div>
    <AppHeader />
    <div class="header-line"></div>
    <main>
      <h1>Welcome to the HomePage</h1>
      <!-- Add your homepage content here -->
    </main>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue'; // Ensure this path is correct

export default {
  name: "HomePageView",
  components: {
    AppHeader,
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Roboto:400,500&display=swap');
@import '@/assets/global.css';

body {
  font-family: 'Roboto', sans-serif;
  background-color: #ffffff; /* White background */
}

.header-line {
  height: 1px;
  background-color: #dddddd; /* Light grey line */
}
</style>
