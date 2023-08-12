<template>
    <div class="edit-show-page">
      <h1>Edit Show</h1>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="movie">Movie</label>
          <select v-model="selectedMovie" id="movie" class="form-control" required>
            <option value="" disabled>Select a movie</option>
            <option v-for="movie in movies" :value="movie.movie_id" :key="movie.movie_id">
              {{ movie.movie_name }}
            </option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="timing">Timing</label>
          <input v-model="timing" type="text" id="timing" placeholder="HH:MM (24H)" class="form-control" required>
        </div>
        
        <div class="form-group">
          <label for="date">Date</label>
          <input v-model="date" type="date" id="date" class="form-control" required>
        </div>
        
        <div class="form-group">
          <label for="ticketPrice">Ticket Price</label>
          <input v-model="ticketPrice" id="ticketPrice" class="form-control" required>
        </div>
  
        <div class="form-group">
          <label for="screenNumber">Screen Number</label>
          <div v-for="screen in screens" :key="screen.screen_id">
            <input
              type="radio"
              :id="'screen_' + screen.screen_id"
              :value="screen.screen_id"
              v-model="selectedScreenId"
              @change="selectScreen(screen.screen_id, screen.screen_capacity, screen.screen_number)"
              required
            />
            <label :for="'screen_' + screen.screen_id">
              Screen {{ screen.screen_number }} (Capacity: {{ screen.screen_capacity }})
            </label>
          </div>
        </div>
  
        <button type="submit" class="btn btn-primary">Update Show</button>
        
      </form>
      
      <div v-if="response_message"
              class= "alert alert-warning alert-dismissible fade show mt-2"
              role="alert">
                <strong> {{ response_message }} </strong>
        </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      show_id: {
        type: String,
        required: true,
      },
    },
  
    data() {
    return {
      showId: this.$route.params.showId, // Fetch the showId from route parameters
      theatreId: this.$route.params.theatreId,
      show: {},
      movies: [],
      screens: [],
      selectedMovie: null,
      timing: '',
      date: '',
      ticketPrice: '',
      selectedScreenId: null,

      response_message: '',
    };
  },

  mounted() {
    this.getShow();
    this.getMovies();
  },
  
    methods: {
      getMovies() {
        const token = localStorage.getItem('access_token');
        fetch('http://127.0.0.1:5000/api/MoviesData', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        })
          .then(response => response.json())
          .then(data => {
            this.movies = data;
          })
          .catch(error => {
            console.error(error);
          });
      },
  
      getShow() {
  const token = localStorage.getItem('access_token');
  fetch(`http://127.0.0.1:5000/api/ShowDetailsApi/${this.showId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  })
    .then(response => response.json())
    .then(data => {
      this.show = data;
      this.selectedMovie = data.movie_id;
      this.timing = data.timing;
      this.date = data.date;
      this.ticketPrice = data.ticket_price;
      this.selectedScreenId = data.screen_id;
    //   this.theaterId = data.theater_id; // Assuming your API returns theater_id in show data

      // Once theaterId is fetched, call the function to fetch screens
      this.getTheaterScreens();
    })
    .catch(error => {
      console.error(error);
    });
},

    getTheaterScreens() {
      // Fetch screens of the selected theater using the theater ID
      const token = localStorage.getItem('access_token');
      fetch(`http://127.0.0.1:5000/api/ScreensApi/${this.theatreId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => response.json())
        .then(data => {
          // Handle the retrieved screen data
          this.screens = data;
        })
        .catch(error => {
          // Handle any errors
          console.error(error);
        });
    },
  
      submitForm() {
        const show = {
          movie_id: this.selectedMovie,
          timing: this.timing,
          date: this.date,
          ticketPrice: this.ticketPrice,
          screenId: this.selectedScreenId,
          screenNumber: this.selectedScreenNumber,
          screenCapacity: this.selectedScreenCapacity,
          theatre_id: this.theatreId
        };

        // console.log("screenCapacity", screenCapacity);
        // console.log("screenNumber", screenNumber);
        console.log(show);
        console.log(this.showId);
  
        const token = localStorage.getItem('access_token');
        fetch(`http://127.0.0.1:5000/api/EditShow/${this.showId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(show),
        })
          .then(response => response.json())
          .then(data => {
            console.log(data);

                    // Show a message after successful update
                    this.response_message = "Show details updated successfully";
                    // Wait for 3 seconds and then redirect to manageShows page
                    setTimeout(() => {
                    this.$router.push('admin/manageShows');
                    }, 3000);
                

          })
          .catch(error => {
            console.error(error);
          });
      },
  
      cancel() {
        this.$router.push('/manageShows');
      },

  
      selectScreen(screenId, screenCapacity, screenNumber) {
        this.selectedScreenId = screenId;
        this.selectedScreenNumber = screenNumber;
        this.selectedScreenCapacity = screenCapacity;
      },
    },
  
    mounted()
    {
    this.getMovies();
    this.getShow();
  },
};
</script>

<style scoped>
.edit-show-page {
  max-width: 600px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1em;
}

label {
  display: block;
  margin-bottom: 0.5em;
}

input, select {
  width: 100%;
  height: 2em;
}

input[type="radio"] {
  transform: scale(0.7);
}

button {
  margin-top: 1em;
}

</style>



