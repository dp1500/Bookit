<template>

  <div>

    <nav class="navbar navbar-expand-lg navbar-light " style="background-color: #6baede;">
  <a class="navbar-brand" href="#">BookIt</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavDropdown">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link" href="/">Home </a>
      </li>

      <li class="nav-item">
        <a class="nav-link" href="/TheatresDisplay">Theatres</a>
      </li>

      <li class="nav-item">
        <a class="nav-link" href="/MyProfile">My Profile</a>
      </li>


      <li class="nav-item">
        <a class="nav-link" href="#"></a>
      </li>

      <!-- <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Dropdown link
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
          <a class="dropdown-item" href="#">Action</a>
          <a class="dropdown-item" href="#">Another action</a>
          <a class="dropdown-item" href="#">Something else here</a>
        </div>
      </li> -->
      
      <li class="nav-item">
          <div class="city-slot">
          <!-- Slot for the current city display -->
          <slot name="city"></slot>
          </div>
      </li>

      <li>
        <div class="nav-item">
          <button v-if="isAuthenticated" class="btn btn-danger btn-sm" @click="logout">Logout</button>
          <button v-else class="btn btn-success btn-sm" @click="openLoginModal">Sign In</button>

        </div>
      </li>

      
      
    </ul>
  </div>

  

  <form >
    <input class="form-control mr-sm-2" type="search" placeholder="Search For Movies" aria-label="Search" v-model="searchQuery" @input="handleSearch" />
    <div class="search-results">
      <!-- <router-link 
          v-for="result in searchResults" 
          :key="result.id"
          :to="{ name: 'MovieDisplay', params: { movieName: result.movie_name } }"
        >
          {{ result.movie_name }}
      </router-link> -->

      <div v-for="result in searchResults" :key="result.id">
        <router-link 
          :to="{ name: 'MovieDisplay', params: { movieName: result.movie_name } }"
        >
          {{ result.movie_name }}
        </router-link>
      </div>

    </div>
    
  </form>

  

</nav>

 <!-- UserLogin Component -->
 <user-login class="user-login-popup" v-if="showUserLoginPopup" v-cloak @userLoggedIn="handleUserLoggedIn" @close-popup="closeLoginModal" @open-sign-up="closeLoginOpenSignIn"></user-login>
        <!-- UserSignUp Component -->
        <user-sign-up class="user-signup-popup" v-if="showUserSignUpPopup" @close-popup="closeSignUpModal" @open-login="closeLoginOpenSignIn" @userSignedUp="closeLoginOpenLogIn"></user-sign-up>
    
        </div>

</template>

<script>

import UserLogin from '../components/UserLogin.vue';
import UserSignUp from '../components/UserSignUp.vue';

export default {
  name: 'NavBar',

  components: { UserLogin, UserSignUp },

  data() {
    return {
      searchQuery: '',
      searchResults: [],
      isAuthenticated: localStorage.getItem('isAuthenticated') === 'true', // read isAuthenticated from local storage

      showUserLoginPopup: false,
      showUserSignUpPopup: false,

      response_message: null,
      errorMessage: null,
    };
  },
  methods: {
    async handleSearch() {
      if (!this.searchQuery) {
        this.searchResults = [];
        return;
      }

      const response = await fetch(`http://localhost:5000/api/searchMovies/${this.searchQuery}`);
      if (response.ok) {
        this.searchResults = await response.json();
        console.log(this.searchResults)
      }
    },

    handleUserLoggedIn() {
      // When the user logs in, close the login popup and set isAuthenticated to true
      this.showUserLoginPopup = false;
      this.isAuthenticated = true;
      this.response_message = "Successfully logged in!";
      this.errorMessage = "";
    },

    openLoginModal() {
    this.showUserLoginPopup = true;
  },

    closeLoginModal() {
      this.showUserLoginPopup = false; // This will hide the login modal
    },
    closeSignUpModal() {
      this.showUserSignUpPopup = false; // This will hide the login modal
    },
    closeLoginOpenSignIn() {
      this.showUserLoginPopup = false; // This will hide the login modal
      this.showUserSignUpPopup = true;
    },
    closeSignUpOpenLogIn() {
      this.showUserLoginPopup = true; // This will hide the login modal
      this.showUserSignUpPopup = false;
    },


    logout() {
      if (window.confirm("Are you sure you want to log out?")) {
      localStorage.removeItem('isAuthenticated'); // remove isAuthenticated from local storage
      localStorage.removeItem('access_token'); // remove access_token from local storage
      this.isAuthenticated = false;
      if (this.$router.currentRoute.path !== '/') {
      this.$router.push('/'); // navigate to HomePage
    } else {
      this.$router.go(0); // Reload the current page
    }
    }
  },
  },
  

}
</script>


<style scoped>
.search-results{
  
  position: absolute;
  background: rgb(255, 255, 255);
  width: 100%;
  z-index: 1;  /* add this line */
}

.search-results div {
  border-bottom: 1px solid #ddd;
  padding: 10px 0;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  direction: ltr;
  text-align: center;
}

form {
  position: relative;
}

.user-login-popup, .user-signup-popup {
  position: fixed;
  /* Center the popup */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000; /* or a higher value if needed */
}

.btn-sm {
    padding: 5px 10px;  /* Adjust as needed */
    font-size: 12px;  /* Adjust as needed */
    margin: 5px 0;  /* Adjust as needed - This will add 5px margin at the top and bottom */
    margin-left: 15px;
    align-self: center; /* This will vertically center the button if the navbar is a flex container */
}

.city-slot {
    /* Your styles here. For example: */
    color: blue;
    padding: 1px;
    /* margin-left: 0%; */
    /* font: 1px; */
}


</style>