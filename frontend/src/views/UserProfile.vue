<template>
  <div>
    <AppHeader />
    <div class="user-profile main-content">
      <h2>Manage Profile</h2>
      <div class="profile-form">
        <div class="avatar-container">
          <img :src="profile.avatar_base64" alt="Avatar" v-if="profile.avatar_base64" class="avatar-image" />
          <button v-if="profile.avatar_base64" @click="deleteImage" class="delete-button">Delete Picture</button>
        </div>
        <div class="form-container">
          <form @submit.prevent="updateProfile">
            <div>
              <label for="bio">Bio:</label>
              <textarea id="bio" v-model="profile.bio" rows="4"></textarea>
            </div>
            <div>
              <label for="avatar">Profile Picture:</label>
              <input type="file" id="avatar" @change="handleImageUpload" />
            </div>
            <div>
              <label for="website">Website:</label>
              <input type="text" id="website" v-model="profile.website_url" />
            </div>
            <div>
              <label for="language1">Favorite Language 1:</label>
              <v-select v-model="profile.default_language_1" :options="languages" searchable placeholder="Select a language"></v-select>
            </div>
            <div>
              <label for="language2">Favorite Language 2:</label>
              <v-select v-model="profile.default_language_2" :options="languages" searchable placeholder="Select a language"></v-select>
            </div>
            <div>
              <label for="language3">Favorite Language 3:</label>
              <v-select v-model="profile.default_language_3" :options="languages" searchable placeholder="Select a language"></v-select>
            </div>
            <div>
              <label for="language4">Favorite Language 4:</label>
              <v-select v-model="profile.default_language_4" :options="languages" searchable placeholder="Select a language"></v-select>
            </div>
            <div>
              <label for="language5">Favorite Language 5:</label>
              <v-select v-model="profile.default_language_5" :options="languages" searchable placeholder="Select a language"></v-select>
            </div>
            <button type="submit" class="action-button">Update Profile</button>
          </form>
        </div>
      </div>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
  </div>
</template>

<script>
import AppHeader from '../components/AppHeader.vue';
import VSelect from 'vue3-select';
import 'vue3-select/dist/vue3-select.css';
import { languages } from '../languages'; // Ensure this path is correct

export default {
  name: 'UserProfile',
  data() {
    return {
      profile: {
        bio: '',
        avatar_base64: '',
        website_url: '',
        default_language_1: '',
        default_language_2: '',
        default_language_3: '',
        default_language_4: '',
        default_language_5: '',
      },
      languages, // Add languages to data
      userId: 3, // Change this to dynamically get the logged-in user's ID
      successMessage: '',
      errorMessage: ''
    };
  },
  components: {
    AppHeader,
    VSelect
  },
  created() {
    this.fetchProfile();
  },
  methods: {
    fetchProfile() {
      fetch(`http://localhost:5000/api/profiles/${this.userId}`)
        .then((response) => response.json())
        .then((data) => {
          this.profile = data;
        })
        .catch((error) => {
          console.error('Error fetching profile:', error);
          this.errorMessage = 'Error fetching profile';
        });
    },
    updateProfile() {
      fetch(`http://localhost:5000/api/profiles/${this.userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.profile),
      })
        .then((response) => response.json())
        .then(() => {
          this.successMessage = 'Profile updated successfully!';
          setTimeout(() => {
            this.successMessage = '';
          }, 3000);
        })
        .catch((error) => {
          this.errorMessage = 'Error updating profile: ' + error.message;
          setTimeout(() => {
            this.errorMessage = '';
          }, 3000);
        });
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.resizeImage(e.target.result, 200, (resizedImage) => {
            this.profile.avatar_base64 = resizedImage;
          });
        };
        reader.readAsDataURL(file);
      }
    },
    deleteImage() {
      this.profile.avatar_base64 = '';
    },
    resizeImage(dataUrl, maxSize, callback) {
      const img = new Image();
      img.src = dataUrl;
      img.onload = () => {
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > maxSize) {
            height *= maxSize / width;
            width = maxSize;
          }
        } else {
          if (height > maxSize) {
            width *= maxSize / height;
            height = maxSize;
          }
        }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);

        callback(canvas.toDataURL());
      };
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Roboto:400,500&display=swap');

.main-content {
  padding: 20px;
  background-color: var(--background-color);
  color: var(--text-color);
}

.user-profile {
  padding: 20px;
  background-color: white; /* Set background to white */
  font-family: var(--main-font-family);
  max-width: 40%; /* Set to 40% width and center */
  margin: auto;
}

h2 {
  margin-bottom: 20px;
}

.profile-form {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.avatar-container {
  flex: none;
}

.avatar-image {
  max-width: 150px;
  border-radius: 50%;
}

.delete-button {
  display: block;
  margin-top: 10px;
  padding: 5px 10px;
  background-color: red;
  color: white;
  border: none;
  cursor: pointer;
  text-transform: uppercase;
  font-weight: bold;
}

.form-container {
  flex: 1;
}

form {
  display: flex;
  flex-direction: column;
}

form div {
  margin-bottom: 10px;
}

form label {
  font-weight: bold;
}

form input[type="text"],
form textarea,
v-select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid var(--header-border-color);
  outline: none;
  font-size: 14px;
  font-family: var(--main-font-family);
}

form button.action-button {
  padding: 10px 20px;
  background-color: var(--button-background-color); /* Turn black when enabled */
  color: white;
  border: none;
  cursor: pointer;
  text-transform: uppercase;
  font-weight: bold;
  width: 100%; /* Full width button */
  height: 40px;
  align-self: flex-start;
}

form button.action-button:hover {
  background-color: var(--accent-color);
}

.success-message {
  color: green;
  margin-top: 10px;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>
