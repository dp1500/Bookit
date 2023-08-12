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
                  <button v-if="!isAuthenticated" @click="handleSignIn">Sign In</button>
                  <button v-if="isAuthenticated" @click="handleSignOut">Log Out</button>
              </template>
          </NavBar>
        </div>

        <h1>Available shows for {{ movie_name }}:</h1>
        <!-- Date selection -->
        <div class="date-selection">
            <label for="show-date">Select date: </label>
            <input type="date" id="show-date" v-model="selectedDate" @change="fetchTheatresAndShows">
        </div>
        <br>
        <br>
        <div v-if="theatres.length === 0" class="no-shows-message">
            <br>
            <h3>No shows Found</h3>
            
        </div>
        <!-- Display theatres and shows here -->
        <div v-for="theatre in theatres" :key="theatre.theatre_id" class="theatre-card">
            <h4>{{ theatre.theatre_name }}</h4>
            <ul>
                <router-link v-for="show in theatre.shows" 
             :key="show.timing" 
             class="btn btn-outline-success"
             :to="show.seats_left !== 0 ? { name: 'FinalBooking', params: { showId: show.show_id } } : null"
             :class="{ disabled: show.seats_left === 0 }"
>
    <h5>Time: {{ show.timing }}</h5>
    <h6 v-if="show.seats_left !== 0">Seats left: {{ show.seats_left }}</h6>
    <p v-else>Houseful</p>
</router-link>
            </ul>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
    name: "MovieShows",
    data() {
        return {
            movieData: null,
            theatres: [],
            selectedCity: localStorage.getItem('selectedCity') || null,
            selectedDate: null,
            movie_name: this.$route.params.movieName,
        }
    },
    components: {
        NavBar,
    },
    async created() {
        const movieName = this.$route.params.movieName;
        // Fetch the movie details
        const movieResponse = await fetch(`http://localhost:5000/api/MovieData/${movieName}`);
        if(movieResponse.ok) {
            this.movieData = await movieResponse.json();
            console.log("movie data is: ", this.movieData)
        } 
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        this.selectedDate = `${year}-${month}-${day}`;

        this.fetchTheatresAndShows();
    },
    methods: {
        async fetchTheatresAndShows() {
            // Fetch the theatres and shows details
            console.log("movie_id is: ", this.movieData.movie_id)
            console.log("selectedCity is: ", this.selectedCity)
            console.log("date is: ", this.selectedDate)
            const showsResponse = await fetch(`http://localhost:5000/api/TheatresShowsApi/${this.movieData.movie_id}/${this.selectedCity}/${this.selectedDate}`);

            if(showsResponse.ok) {
                this.theatres = await showsResponse.json();
                console.log("response okay   theatres data is: ", this.theatres)
            }
        }
    },
    computed: {
        filteredTheatres() {
            // Filter the theatres to only include those with shows on the selected date
            return this.theatres.filter(theatre => {
                return theatre.shows.some(show => show.date === this.selectedDate);
            });
        }
    }
}
</script>
 

<style scoped>
.movie-title {
  font-size: 2em;
  text-align: center;
  margin: 20px 0;
}

.theatre-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.theatre-info {
  width: 70%;
}

.theatre-info h3 {
  margin: 0;
  margin-bottom: 10px;
}

.show-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
  margin-left: 10px;
}

.theatre-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ccc;
  padding: 15px; /* reduced padding for less height */
  border-radius: 10px;
  margin-bottom: 20px;
  width: 80%;
  margin: auto;
  font-size: 1.3em; /* reduce the font size inside the card */
}

.theatre-card .btn {
  font-size: 0.7em; /* reduce the button font size */
  padding: 8px 12px; /* reduce button padding */
}


.disabled {
    pointer-events: none;
    cursor: default;
    opacity: 0.6;
}

#app {
  background-color: #FAF9F6;
  min-height: 100vh;
}

</style>