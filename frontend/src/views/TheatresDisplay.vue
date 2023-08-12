<template>
    <div id="app">
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
    
        <div class="container mt-4">
        <h3 class="mb-4">Theatres in the city of {{ selectedCity }}</h3>
        <div class="row">
            <div class="col-md-6 col-lg-4 mb-4" v-for="theatre in theatres" :key="theatre.theatre_id">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                <h5 class="card-title">{{ theatre.theatre_name }}</h5>
                <h6 class="card-subtitle mb-2 text-muted">{{ theatre.address }}</h6>
                <p class="card-text">
                    <strong>City:</strong> {{ theatre.city }}
                    <br>
                    <br>
                    <strong>Screens:</strong> {{ theatre.screens }}
                </p>
                </div>
                <div class="card-footer">
                <router-link :to="{ name: 'DisplayShows', params: { theatreId: theatre.theatre_id } }" class="btn btn-primary">View Shows</router-link>
                </div>
            </div>
            </div>
        </div>
        </div>
  </div>
</template>
  
<script>

import NavBar from '../components/NavBar.vue';

export default {
  data() {
    return {
      selectedCity: localStorage.getItem('selectedCity') || 'DefaultCity',
      cities: ['Delhi NCR', 'Mumbai', 'Pune', 'Chennai', 'Bangalore', 'Hyderabad'],  // Replace this with actual city list
      theatres: [],
    };
  },

  components: {
    NavBar,
    
  },

  methods: {
    fetchTheatres() {
        const city = this.selectedCity;
fetch(`http://127.0.0.1:5000/api/TheatresInCity/${city}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
})
        .then((response) => response.json())
        .then((data) => {
          // Handle the retrieved theatre data
          this.theatres = data;
        })
        .catch((error) => {
          // Handle any errors
          console.error(error);
        });
    },
    changeCity() {
      // Update selected city in local storage
      localStorage.setItem('selectedCity', this.selectedCity);

      // Fetch theatres for the selected city
      this.fetchTheatres();
    },
  },
  mounted() {
    // Fetch theatres for the selected city when the component is mounted
    this.fetchTheatres();
  },
};
</script>

<style scoped>
.city-display {
    width: 90px;
    margin: 10px auto;
    /* margin-bottom: 10px; */
}

.custom-select {
    background: #c3def1;
    border: none;
    border-radius: 2px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 2.5px 2.5px;
    font-size: 15px;
    color: #333;
    text-align: center;
}

#app {
  background-color: #FAF9F6;
  min-height: 100vh;
}

</style>