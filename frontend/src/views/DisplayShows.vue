<template>
    <div id="app">
      <NavBar>
        <!-- Auth slot -->
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
      
      <div class="container mt-4">
        <!-- Theatre Details -->
        <div>
          <h2>{{ theatre.theatre_name }}</h2>
          <p>{{ theatre.address }}</p>
          <p>{{ theatre.city }}</p>
          <p>{{ theatre.screens }} Screens</p>
        </div>
  
        <hr>
  
        <!-- Shows List -->
        <h3>Shows Available</h3>
        <div class="row">
          <div v-if="shows.length" class="col-md-4">
          <div  v-for="show in shows" :key="show.show_id">
            <div class="card mb-4">
              <div class="card-body">
                <h5 class="card-title">{{ show.movie_name }}</h5>
                <p class="card-text">
                  Rating: {{ show.rating }}
                  <br>
                  <br>
                  Date: {{ show.date }}
                  <br>
                  <br>
                  Time: {{ show.timing }}
                  <br>
                  <br>
                  Ticket Price: {{ show.ticket_price }}
                  <br>
                  <br>
                  Seats Left: {{ show.seats_left }}
                </p>
                <button @click="bookTicket(show.show_id)" class="btn btn-primary">Book Ticket</button>
              </div>
            </div>
          </div>
          </div>
            <div v-else class="col-md-12">
               <p>This theatre currently does not have any shows.</p>
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
        theatre: {},  
        shows: [],
        // Replace the following line with actual auth check
        isAuthenticated: false
      };
    },
    components: {
      NavBar
    },
    methods: {
      fetchTheatreData() { 
        const theatreId = this.$route.params.theatreId;
        fetch(`http://127.0.0.1:5000/api/UserTheatreData/${theatreId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response => response.json())
        .then(data => {
          this.theatre = data; 
        })
        .catch(error => {
          console.error(error);
        });
      },


      fetchShowData() {
            const theatreId = this.$route.params.theatreId;
            fetch(`http://127.0.0.1:5000/api/ShowsApi/${theatreId}`, { 
                method: 'GET',
                headers: {
                'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Map each show to a promise that fetches the movie data and resolves to the combined data
                const showPromises = data.map(show =>
                fetch(`http://127.0.0.1:5000/api/UserMovieData/${show.movie_id}`, {
                    method: 'GET',
                    headers: {
                    'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(movie => {
                    // Merge show and movie data
                    return {
                    ...show,
                    movie_name: movie.movie_name,
                    rating: movie.rating
                    };
                })
                );
                
                // Wait for all promises to complete before updating this.shows
                Promise.all(showPromises)
                .then(shows => {
                    this.shows = shows;
                })
                .catch(error => {
                    console.error(error);
                });
            })
            .catch(error => {
                console.error(error);
            });
            },


            bookTicket(showId) {
            // Get the 'access_token' from the localStorage
            const accessToken = localStorage.getItem('access_token');

            // If the 'access_token' is not found, prompt them to log in
            if (!accessToken) {
                alert('Please log in to book tickets.');
                return;
            }

            // If the 'access_token' is found, redirect to the final booking page
            this.$router.push(`/FinalBooking/${showId}`);
        },
      // Replace the following methods with actual auth handling
      handleSignIn() {
        this.isAuthenticated = true;
      },
      handleSignOut() {
        this.isAuthenticated = false;
      }
    },
    mounted() {
      this.fetchTheatreData();
      this.fetchShowData();
    }
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
  