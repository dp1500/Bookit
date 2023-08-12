<template>
  <div id="app" >

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
    <h1 class="mb-4">Booking Summary</h1>

    <div class="row">
      <div class="col-lg-6 mb-4">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title">Show Details:</h2>
            <div class="card-text">
              <div class="card-item">
                <strong>Movie:</strong> {{ show.movie_name }}
              </div>
              <div class="card-item">
                <strong>Theatre:</strong> {{ show.theatre_name }}
              </div>
              <div class="card-item">
                <strong>Address:</strong> {{ show.address }}
              </div>
              <div class="card-item">
                <strong>City:</strong> {{ show.city }}
              </div>
              <div class="card-item">
                <strong>Show Timing:</strong> {{ show.timing }}
              </div>
              <div class="card-item">
                <strong>Show Screen:</strong> {{ show.screenNumber }}
              </div>
              <div class="card-item">
                <label for="tickets"><strong>How many tickets you want to book?</strong> </label>
                <input type="number" id="tickets" v-model="tickets" min="1" :max="show.seats_left">
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-6 mb-4">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title">Bill Details:</h2>
            <div class="card-text">
              <div class="card-item">
                <strong>Booking for:</strong> {{ userName }}
              </div>
              <div class="card-item">
                <strong>Ticket Price:</strong> {{ show.ticket_price }}
              </div>
              <div class="card-item">
                <strong>Tickets Booked:</strong> {{ tickets }}
              </div>
              <div class="card-item">
                <strong>Total Price:</strong> {{ totalPrice }}
              </div>
              <div class="card-item">
                <strong>Tickets booked on:</strong> {{ today }}
              </div>
              <button @click="handleFinalBooking" class="btn btn-primary mt-2">Book Ticket</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="response_message"
      class= "alert alert-warning alert-dismissible fade show mt-2"
      role="alert">
        <strong> {{ response_message }} </strong>
    </div>
  </div>
</template>
  
  <script>

import NavBar from '../components/NavBar.vue';

  export default {
    data() {
      return {
        show: null,
        tickets: 1,
        userName: null,
        userId: null,
        today: '',
        show_id: this.$route.params.showId,
        response_message: '',

        isAuthenticated: false, // Represents the user's authentication state
        selectedCity: localStorage.getItem('selectedCity') || null,
      };
    },

    components: {
      NavBar
    },

    async created() {
      const showId = this.$route.params.showId;

      // Fetch the show details
      const responseShow = await fetch(`http://localhost:5000/api/ShowDetailsApi/${showId}`);
      if (responseShow.ok) {
        this.show = await responseShow.json();
      }

      // Fetch the user details
      const responseUser = await fetch('http://localhost:5000/api/ProfileData', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      if (responseUser.ok) {
        const userData = await responseUser.json();
        console.log("from async created the user data got is: ", userData)
        this.userName = userData.name;
        this.userId = userData.user_id;
      }

      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');
      this.today = `${year}-${month}-${day}`;
    },


    computed: {
      totalPrice() {
        return this.show ? this.show.ticket_price * this.tickets : 0;
      },
    },
    methods: {
      async handleFinalBooking() {
        console.log("user id is: ", this.userId)
        const bookingData = {
          user_id: this.userId,
          show_id: this.show_id,
          booking_date: this.today,
          ticket_count: this.tickets,
          total_price: this.totalPrice,
        };

        
  
        const response = await fetch('http://localhost:5000/api/BookTicketsApi', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
          body: JSON.stringify(bookingData),
        });
  
        if (response.ok) {

          this.response_message = "succesfully Booked tickets, redirecting to Home Page";
          setTimeout(() => {
                    this.$router.push({
                        name:'HomePage',
                        
                    });
                    }, 3000);
          // Redirect to a different page or clear the input
        } else {
          alert('Booking failed');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .card-text .card-item {
    margin-bottom: 1em; /* adjust as needed */
    font-size: 1.2em; /* adjust as needed */
  }
  
  .card-item input[type="number"] {
    width: 100%;
    margin-top: 0.3em;
  }
  
  .card-item label {
    display: block;
    font-size: 1.2em; /* adjust as needed */
  }
  
  .card-body {
    line-height: 1.5; /* adjust as needed */
  }

  #app {
  background-color: #FAF9F6;
  min-height: 100vh;
}

  
  </style>