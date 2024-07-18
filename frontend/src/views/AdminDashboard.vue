<template>
  <div>
    <AppHeader />
    <SubHeader />
    <div class="main-content">
      <!-- Add the main content here -->
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import SubHeader from '@/components/SubHeader.vue';

export default {
  name: 'AdminDashboard',
  components: {
    AppHeader,
    SubHeader,
  },
};
</script>

<style scoped>
.main-content {
  padding: 20px;
  background-color: var(--background-color);
  color: var(--text-color);
}
</style>
