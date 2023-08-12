<template>
  <div id="app">
      <div>
          <NavBar>
              <template v-slot:city>
                  <div class="city-display" v-if="selectedCity">
                      {{ selectedCity }}
                  </div>
              </template>
              <template v-slot:auth>
              <button v-if="!isAuthenticated" @click="showUserLoginPopup = true">Sign In</button>
              <button v-if="isAuthenticated" @click="handleSignOut">Log Out</button>
            </template>
          </NavBar>
      </div>
      <div class="container movie-container">
          <div class="card movie-card">
              <div class="row no-gutters">
                  <div class="col-md-4">
                      <img :src="movieData.image_url" class="card-img" alt="Movie Poster">
                  </div>
                  <div class="col-md-8">
                      <div class="card-body">
                          <!-- <h5 class="card-title">{{ movieData.movie_name }}</h5>
                          <p class="card-text">{{ movieData.description }}</p>
                          <p class="card-text"><small class="text-muted">Release Date: {{ movieData.releaseDate }}</small></p> -->

                          <h2 class="card-title">{{ movieData.movie_name }}</h2>
                          <p class="card-text movie-description">{{ movieData.description }}</p>
                          <p class="card-text genres" >Genres: {{ Array.isArray(movieData.genres) ? movieData.genres.join(', ') : movieData.genres }}</p>
                          <p class="card-text release-date"><small class="text-muted">Release Date: {{ movieData.releaseDate }}</small></p>
                          <p class="card-text rating">Rating: {{ movieData.rating }}</p>
                                                  
                            <br>

                          <!-- <h2 class="card-title">{{ movieData.movie_name }}</h2>
                        <p class="card-text">{{ movieData.description }}</p>
                        <p class="card-text"><small class="text-muted">Release Date: {{ movieData.releaseDate }}</small></p> -->

                        <!-- <p class="card-text">Rating: {{ movieData.rating }}</p>
                        <p class="card-text">Genres: {{ movieData.genres.join(', ') }}</p> -->

                          <!-- <button v-if="isAuthenticated" @click="bookShow" class="btn btn-primary">Book a Show</button>
                          <button v-else @click="handleSignIn" class="btn btn-primary">Sign in to Book Ticket</button> -->
                          <div v-if="!showUserLoginPopup" class="movie-card">
                            <!--...Your movie card...-->
                            <button class="btn btn-primary btn-sm" @click="handleBookNow">Book Now</button>
                          </div>

                          <user-login v-if="showUserLoginPopup" v-cloak @userLoggedIn="handleUserLoggedIn" @close-popup="closeLoginModal" @open-sign-up="closeLoginOpenSignIn"></user-login>
                          <!-- UserSignUp Component -->
    <user-sign-up
      v-if="showUserSignUpPopup"
      @close-popup="closeSignUpModal"
      @open-login="closeSignUpOpenLogIn"
      @userSignedUp="closeSignUpOpenLogIn"
    />
                      </div>
                  </div>
                  <div v-if="response_message"
              class= "alert alert-warning alert-dismissible fade show mt-2"
              role="alert">
                <strong> {{ response_message }} </strong>
            </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue' // import the Navbar component

import UserLogin from '../components/UserLogin.vue';

import UserSignUp from '../components/UserSignUp.vue';

export default {
  name: "MovieDisplay",
  data() {
      return {
          movieData: null,
          // isAuthenticated: false, // Represents the user's authentication state
          isAuthenticated: localStorage.getItem('isAuthenticated') === 'true', // read isAuthenticated from local storage
          selectedCity: localStorage.getItem('selectedCity') || null,
          showUserLoginPopup: false,
          showUserSignUpPopup: false,

          response_message: '',

          movieName: this.$route.params.movieName,
      };
  },

  components: { 
      NavBar,
      UserLogin,
      UserSignUp,
  },

  created() {
      const movieName = this.$route.params.movieName;
      // Fetch the movie details from your API
      fetch(`http://localhost:5000/api/MovieData/${movieName}`, {
          method: 'GET'
      })
      .then(response => response.json())
      .then(data => {
          this.movieData = data;
      })
      .catch(error => {
          console.error(error);
      });
  },

  methods: {
      handleSignIn() {
          // Logic to show Sign In / Sign Up pop-up
      },

      handleBookNow() {
        console.log("handlebooking called")
        console.log(this.isAuthenticated)

            if (this.isAuthenticated) {
                // If user is authenticated, redirect to the booking page
                console.log("inside is authenticated");
                

                // const movieName = this.$route.params.movieName;

                console.log("movieName:", this.movieName);

                console.log("hello")

                setTimeout(() => {
                    this.$router.push({
                        name:'MovieShows',
                        params: { movieName: this.movieName }

                    });
                    }, 3000);

                    
            } else {
                // If user is not authenticated, show the login popup
                this.showUserLoginPopup = true;
            }
        },

        handleUserLoggedIn() {
            // When the user logs in, close the login popup and set isAuthenticated to true
            this.showUserLoginPopup = false;
            this.isAuthenticated = true;
            this.response_message = "succesfully logged in, redirecting to movie shows";
                  this.errorMessage ="";
                  const movieName = this.$route.params.movieName;

                  setTimeout(() => {
                    this.$router.push({
                        name:'MovieShows',
                        params: { movieName: this.movieName }

                    });
                    }, 3000);
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
    }

      // bookShow() {
      //     this.$router.push({ name: 'BookShow', params: { movieName: this.movieData.movie_name } })
      // }
  }
};
</script>

<style scoped>
  .card {
    width: 95%;  /* adjust according to your requirement */
    height: 70%;
    margin: auto;
  }
  
  /* If the card-img needs to be a specific height */
  .card-img {
    height: 420px;  /* change as required */
    width: 265px;  /* change as required */
    object-fit: cover; 
    /* This will make sure the image covers the area without stretching */
  }

  /* Rest of your CSS */
  /* [v-cloak] { */
  /* display: none;
} */

.btn-primary {
  background-color: #007BFF; 
   /* Adjust to the bluish color you prefer */
}

.card-title {
    font-size: 24px;
    margin-bottom: 10px;
  }

  .card-body {
  text-align: left; /* Align the text to the left */
}

.card-text {
  color: black; /* Make the text color black */
}

.movie-description {
  line-height: 1.5; /* Add line spacing to the description */
  text-align: justify; /* Justify the text to fill the space */
}

.genres{
  font: 25px;
}

  .book-now {
    background-color: #007BFF; 
    /* Adjust to the bluish color you prefer */
  }

  #app {
  background-color: #FAF9F6;
  min-height: 100vh;
}

</style>
