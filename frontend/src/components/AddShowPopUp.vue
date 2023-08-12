<template>
    <div class="add-show-form">
       
      <div class="modal">
        <button class="close-button" @click="$emit('close-popup')">✕</button>
        <div class="modal-content">
          <h3>Add Show</h3>

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

            <br>

            <!-- <div class="form-group">
              <label for="screenNunber">Screen Number</label>
              <input v-model="screenNunber"  id="screenNunber" class="form-control" required>
            </div> -->

                    <div class="form-group">
              <label for="screenNumber">Screen Number</label>
              <!-- Use radio buttons for screen selection -->
              <div v-for="screen in screens" :key="screen.screen_id">
                <input
                                type="radio"
                  :id="'screen_' + screen.screen_id"
                  :value="screen.screen_id"
                  v-model="selectedScreenId"
                  @change="selectScreen(screen.screen_id, screen.screen_capacity, screen.screen_number)"
                  required
                />
                <label :for="`screen-${screen.screenNumber}`">
                  Screen {{ screen.screen_number }} (Capacity: {{ screen.screen_capacity }})
                </label>
              </div>
            </div>

            <br>
            <!-- @submit.prevent="submitForm" -->
            <div class="form-group">
              <button  @click="submitForm"  class="btn btn-primary" >Add</button>
              <button @click="$emit('cancel')" type="button" class="btn btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {

    props: {
    theaterId: {
      type: Number,
      required: true,
    },
  },
    
  data() {
    return {
      movies: [], // Array to store the movie options
      selectedMovie: '', // Selected movie ID
      timing: '',
      date: '',
      ticketPrice: '',
      screenNunber: null,

      screens: [], // Array to store the screens of the selected theater
      selectedScreenId: null, // Selected screen ID
      selectedScreenNumber: null,
      selectedScreenCapacity: null,
    };
  },
  mounted() {
    // Call the getMovies function to fetch movie options
    this.getMovies();
    this.getTheaterScreens();
  },
  methods: {
    getMovies() {
      const token = localStorage.getItem('access_token');
      fetch('http://127.0.0.1:5000/api/MoviesData', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => response.json())
        .then(data => {
          // Handle the retrieved movie data
          this.movies = data;
        })
        .catch(error => {
          // Handle any errors
          console.error(error);
        });
    },

      // Fetch screens of the selected theater using the theater ID
    getTheaterScreens() {
      const token = localStorage.getItem('access_token');
      const theaterId = this.theaterId; // Get the selected theater ID from the prop

      console.log("theatre id is : " , theaterId)

      fetch(`http://127.0.0.1:5000/api/ScreensApi/${theaterId}`, {
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
      console.log("submit form called")
      console.log("selected screen number is ", this.selectedScreenNumber)
      // Create a show object from the form data
      const show = {
        movie_id: this.selectedMovie,
        timing: this.timing,
        date: this.date,
        ticketPrice: this.ticketPrice,
        screenNumber: this.selectedScreenNumber,
        show_capacity: this.selectedScreenCapacity,
        theatre_id: this.theaterId,

      };

        const token = localStorage.getItem('access_token');
         fetch('http://127.0.0.1:5000/api/ShowsApi', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(show)
            })
        .then(response => response.json())
        .then(data => {
        // Handle the response from the backend
        console.log(data); // Optional: Log the response for debugging

            this.$emit('close');
          
        
        // Perform any further actions as needed
        })
        .catch(error => {
        // Handle any errors
        console.error(error);
        });

    //   // Emit an event to the parent component to pass the show data
    //   this.$emit('add-show', show);

      // Reset form inputs
      this.selectedMovie = '';
      this.timing = '';
      this.date = '';
      this.ticketPrice = '';
      this.screenNunber = '';
    },
    closePopup() {
      // Emit an event to the parent component to close the pop-up
      this.$emit('close-popup');
    },
    selectScreen(screenId, screenCapacity, screenNumber) {
    this.selectedScreenId = screenId;
    this.selectedScreenNumber = screenNumber;
    this.selectedScreenCapacity = screenCapacity;
  },
  },

  watch: {
    selectedTheaterId() {
      this.getTheaterScreens();
    }
  }
  };
  </script>
  
  <style scoped>



  .add-show-form {

    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    max-width: 400px;
    width: 90%;
    height: 70%;
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    /* display: flex;
    align-items: center;
    justify-content: center;
    height: 100%; */
  }
  
  .modal {
    /* background-color: rgba(0, 0, 0, 0.5);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0; */

    
    display: flex;
    /* align-items: center; */
    /* justify-content: center; */
/* 
    position: fixed;
    top: 30%;
    left: 51%;
    transform: translate(-50%, -50%);
    max-width: 400px;
    height
    width: 100%;
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); */
    
  }
  
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
  }

  .close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  font-weight: bold;
  color: #555;
  background: transparent;
  border: none;
  cursor: pointer;
}
  </style>
  