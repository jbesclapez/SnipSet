// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import { theme } from './theme';
import { VueReCaptcha } from 'vue-recaptcha-v3';
import './assets/global.css';  // Import the global stylesheet

// Inject theme variables as CSS variables
const themeStyles = document.createElement('style');
themeStyles.innerHTML = `
  :root {
    --primary-color: ${theme.primaryColor};
    --secondary-color: ${theme.secondaryColor};
    --accent-color: ${theme.accentColor};
    --background-color: ${theme.backgroundColor};
    --text-color: ${theme.textColor};
    --muted-text-color: ${theme.mutedTextColor};
    --header-background-color: ${theme.headerBackgroundColor};
    --header-border-color: ${theme.headerBorderColor};
    --dropdown-background-color: ${theme.dropdownBackgroundColor};
    --dropdown-hover-color: ${theme.dropdownHoverColor};
    --button-background-color: ${theme.buttonBackgroundColor};
    --active-link-color: ${theme.activeLinkColor};
    --main-font-family: 'Roboto', sans-serif;
  }
`;
document.head.appendChild(themeStyles);

const app = createApp(App);

app.use(store);
app.use(router);
app.use(VueReCaptcha, { siteKey: '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI' });

app.mount('#app');
