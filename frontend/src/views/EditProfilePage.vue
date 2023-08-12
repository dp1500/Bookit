<template>
    <div>
                <div>
                <NavBar>
                <template v-slot:city>
                <div class="city-display" v-if="selectedCity">
                {{ selectedCity }}
                </div>
                </template>
                <template v-slot:auth>
                <button v-if="!isAuthenticated" @click="handleSignIn">Sign In</button>
                <button v-if="isAuthenticated" @click="handleSignOut">Log Out</button>
                </template>
            </NavBar>
            </div>

    <div class="container">
            <h1>Edit Profile</h1>
            <form @submit.prevent="handleSubmit" class="edit-form">
            <div class="input-group">
                <label for="name">New Name:</label>
                <input id="name" v-model="name" type="text" />
            </div>
            <div class="input-group">
                <label for="username">New Username:</label>
                <input id="username" v-model="username" type="text" />
            </div>
            <div class="input-group">
                <label for="email">New Email:</label>
                <input id="email" v-model="email" type="email" />
            </div>
            <div class="input-group">
                <label for="password">Current Password:</label>
                <input id="password" v-model="password" type="password" />
            </div>
            <div class="input-group">
                <label for="newPassword">New Password:</label>
                <input id="newPassword" v-model="newPassword" type="password" />
            </div>
            <button type="submit">Update</button>
            </form>
        </div>
    </div>
  </template>
  
  <script>
    import NavBar from '@/components/NavBar.vue'
  export default {

    components: {
      NavBar
    },

    data() {
        
      return {
        name: "",
        username: "",
        email: "",
        password: "",
        newPassword: "",

        isAuthenticated: false, // Represents the user's authentication state
        selectedCity: localStorage.getItem('selectedCity') || null,
      };
    },
    methods: {
        async handleSubmit() {
        const token = localStorage.getItem('access_token');
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/ProfileData`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({
                    name: this.name,
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    new_password: this.newPassword,
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            } else {
                this.password = "";
                this.newPassword = "";
                alert("Profile updated successfully");
                localStorage.removeItem('access_token'); // Remove token
                this.$router.push('/'); // Redirect to home

            }
        } catch (error) {
            alert(`An error occurred: ${error.message}`);
        }
    }
},
  }
  </script>
  
  <style scoped>
  .container {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}

.edit-form {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
}

.input-group input {
  width: 100%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button {
  display: block;
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 4px;
  background: #007BFF;
  color: white;
  cursor: pointer;
}
  </style>
  