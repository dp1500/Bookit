
<template>
    <div style="background-color: #FAF9F6;">
      <div>
        <NavBar>
          <template v-slot:city>
                <div class="city-display" v-if="selectedCity">
                    <select v-model="selectedCity" class="form-control custom-select" @change="changeCity">
                    <option disabled value="">Please select a city</option>
                    <option v-for="city in cities" :key="city">{{ city }}</option>
                </select>
                </div>
            </template>
        <template v-slot:auth>
          <button v-if="!isAuthenticated" @click="handleSignIn">Sign In</button>
          <button v-if="isAuthenticated" @click="handleSignOut">Log Out</button>
        </template>
      </NavBar>
      </div>

      <div class="filter-container">
      <div>
        <label for="genre-select">Genre:</label>
        <select id="genre-select" v-model="selectedGenre">
          <option value="">All</option>
          <option v-for="genre in genreOptions" :key="genre">{{ genre }}</option>
        </select>
      </div>
      <div>
        <label for="rating-select">Rating:</label>
        <select id="rating-select" v-model="selectedRating">
          <option value="">All</option>
          <option v-for="rating in ratingOptions" :key="rating">{{ rating }}</option>
        </select>
      </div>
    </div>

      <div class="container">
      <div class="row">
        <div class="col-lg-3" v-for="movie in filteredMovies" :key="movie.id">
          <!-- <div class="card mt-4"> -->
            <div class="card small-card">
            <img class="card-img-top" :src="movie.image_url" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">{{ movie.movie_name }}</h5>
              <p class="card-text">Release Date: {{ movie.releaseDate }}</p>
              <p class="card-text">Rating: {{ movie.rating }}</p>
              <p class="card-text" >Genres: {{ movie.genres }}</p>
              <router-link :to="{ name: 'MovieDisplay', params: { movieName: movie.movie_name } }" class="btn btn-primary">Book Now</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>


      <CityPopup v-if="showCityPopup" @selectCity="handleSelectCity" @closePopup="handleClosePopup" />
    </div>
  </template>
  
  <script>

import NavBar from '@/components/NavBar.vue' // import the Navbar component
import CityPopup from '../components/CityPopup.vue';
  
  export default {

    name: 'MoviesDisplay',
    props: ['movieName'],

    data() {
      return {
        showCityPopup: true,
        isAuthenticated: false, // Represents the user's authentication state
        selectedCity: localStorage.getItem('selectedCity') || null,
        movies: [],

        cities: ['Delhi NCR', 'Mumbai', 'Pune', 'Kolkata', 'Bangalore', 'Hyderabad', 'Chennai'],

        selectedGenre: null,
        selectedRating: null,
        genreOptions: [
                      'Action', 'Drama', 'Adventure', 'Fiction', 'Sci-Fi',
                      'History', 'Documentary', 'Romance', 'Comedy', 'Horror'
                    ],

        ratingOptions: [9, 8, 7, 6, 5],

      };
    },
    watch: {
    selectedCity(newCity, oldCity) {
      // When selectedCity changes, update the local state
      this.selectedCity = newCity;
    },
  },
    components: { 
      CityPopup,
      NavBar
    },
    methods: {
      handleSelectCity(city) {
        // Handle selected city
        console.log('Selected city:', city);
        // You can perform further actions like making an API request to the backend or updating the state.
        
        // For example, you can store the selected city in a Vuex store or local storage:
        // this.$store.commit('setSelectedCity', city);
        // or
        // localStorage.setItem('selectedCity', city);
        
        // After handling the city selection, you can close the popup
        this.handleClosePopup();
      },
      handleClosePopup() {
        // Close the popup
        this.showCityPopup = false;
      },
      handleSignIn() {
      // Sign the user in
      // In your actual application, you would call your backend API here
      this.isAuthenticated = true;
    },
    handleSignOut() {
      
    // Call the Logout API
    fetch('http://localhost:5000/api/logout', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: localStorage.getItem('username'),
      })
    })
      .then(response => {
        if (response.ok) {
          // If the API call is successful, sign the user out on the frontend
          this.isAuthenticated = false;
          localStorage.setItem('isAuthenticated', false);
        } else {
          console.error('Logout API call failed');
        }
      })
      .catch(error => {
        console.error('Logout API call failed:', error);
      });

    },
    changeCity() {
      // Update selected city in local storage
      localStorage.setItem('selectedCity', this.selectedCity);
    },
    },
    mounted() {
      // localStorage.removeItem('selectedCity');
  this.selectedCity = localStorage.getItem('selectedCity');
  // Assuming you store the user's authentication status in localStorage
  this.isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
    },

    created() {
    fetch('http://localhost:5000/api/MoviesData', {
      method: 'GET'
    })
      .then(response => response.json())
      .then(data => {
        this.movies = data.map(movie => ({
            ...movie,
            rating: movie.rating === null ? 0 : movie.rating
        }));
        console.log(this.movies);
      })
      .catch(error => {
        console.error(error);
      });
  },

  computed: {
  filteredMovies() {
    console.log("Selected Rating: ", this.selectedRating);
    console.log("Parsed Selected Rating: ", Number(this.selectedRating));

    return this.movies.filter(movie => {
    const genreMatch = this.selectedGenre ? movie.genres.includes(this.selectedGenre) : true;
    const ratingMatch = this.selectedRating ? Number(movie.rating) >= Number(this.selectedRating) : true;
    return genreMatch && ratingMatch;
    });
  },
  }

  };
  </script>
  
<style>


.small-card {
  width: 82%; /* Reduce the width of the card */
  margin: auto; /* Center the card in its column */
  margin-bottom: 25px;
}

.card-text {
  line-height: 0.7;  /* Adjust this value to increase or decrease line spacing */
}

.city-display {
    width: 100px;
    size: 10px;
    margin: 0px auto;
    /* margin-bottom: 10px; */
    font-size: 1px;
}

.card-title {
    height: 40px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2; /* Show ellipsis after two lines */
    -webkit-box-orient: vertical;
}


.card-body {
  font-size: 14px;
}

/* .card-text{
  margin-top: px;
} */

.genre-tag {
    margin-bottom: 1px;
}

.custom-select {
    background: #c3def1;
    border: none;
    border-radius: 2px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 1.5px 1.5px;
    font-size: 15px;
    color: #333;
    text-align: center;
}

.filter-container {
  display: flex;
  justify-content: space-around;
  margin: 20px 0;
}

.filter-container div {
  display: flex;
  align-items: center;
}

.filter-container label {
  margin-right: 10px;
}




</style>