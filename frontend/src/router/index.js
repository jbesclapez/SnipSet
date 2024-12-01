// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Signup from '../views/Signup.vue';
import CreateAccount from '../views/CreateAccount.vue';
import CreateAccountWithEmail from '../views/CreateAccountWithEmail.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/create-account',
    name: 'CreateAccount',
    component: CreateAccount,
  },
  {
    path: '/create-account-email',
    name: 'CreateAccountWithEmail',
    component: CreateAccountWithEmail,
  },
  {
    path: '/',
    redirect: '/login',
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
