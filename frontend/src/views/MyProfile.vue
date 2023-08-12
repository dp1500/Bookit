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
      <section class="h-100 gradient-custom-2">
        <div class="container w-auto py-4 h-100">
          <div class="row d-lg-flex justify-content-center align-items-center h-100 ">
            <div class="col col-lg-9 col-xl-12">
              <div class="card">
                <div class="rounded-top text-white d-flex justify-content-between" style="background-color: #000; height:200px;">
  <div class="ms-3" style="margin-top: 130px;">
    <h4>name: {{ user_data.name }}</h4>
    <h5>username: {{ user_data.username }}</h5>
  </div>
  <button class="edit-profile" @click="handleEditProfile">Edit Profile</button>
</div>


               <div class="card-body p-4 text-black">
                <h3>Current Bookings</h3>
                <div v-if="currentBookings.length === 0">
                  No current bookings. <router-link to="/">Watch newest movies</router-link>
                </div>
                <div v-else class="d-flex flex-wrap">
                  <div class="booking-card m-2" v-for="booking in currentBookings" :key="booking.booking_id">
                    <div class="booking-card-header">
                      <h5>{{ booking.movie_name }}</h5>
                    </div>
                    <div class="booking-card-body">
                      <!-- <p>Date: {{ formatDate(booking.booking_date) }}</p>
                      <p>Theatre: {{ booking.theatre_name }}</p>
                      <p>Tickets booked: {{ booking.ticket_count }}</p>
                      <p>Total price: {{ booking.total_price }}</p> -->

                        <div class="card-text">
                            <div class="card-item">
                              <strong>Date:</strong> {{ formatDate(booking.booking_date) }}
                            </div>
                            <div class="card-item">
                              <strong>Theatre:</strong> {{ booking.theatre_name }}
                            </div>
                            <div class="card-item">
                              <strong>Tickets booked:</strong> {{ booking.ticket_count }}
                            </div>
                            <div class="card-item">
                              <strong>Total price:</strong> {{ booking.total_price }}
                            </div>
                        </div>
                    </div>
                  </div>
                </div>

                <hr>


                <h3>Booking History</h3>
                  <div v-if="bookingHistory.length === 0">
                    No bookings yet.
                  </div>
                  <div v-else class="d-flex flex-wrap">
                    <div class="booking-card m-2" v-for="booking in bookingHistory" :key="booking.booking_id">
                      <div class="booking-card-header">
                        <h5>{{ booking.movie_name }}</h5>
                      </div>
                      <div class="booking-card-body">
                        
                        <!-- <p>Date: {{ formatDate(booking.booking_date) }}</p>
                        <p>Theatre: {{ booking.theatre_name }}</p>
                        <p>Tickets booked: {{ booking.ticket_count }}</p>
                        <p>Total price: {{ booking.total_price }}</p> -->

                        <div class="card-text">
                            <div class="card-item">
                              <strong>Date:</strong> {{ formatDate(booking.booking_date) }}
                            </div>
                            <div class="card-item">
                              <strong>Theatre:</strong> {{ booking.theatre_name }}
                            </div>
                            <div class="card-item">
                              <strong>Tickets booked:</strong> {{ booking.ticket_count }}
                            </div>
                            <div class="card-item">
                              <strong>Total price:</strong> {{ booking.total_price }}
                            </div>
                        </div>


                      </div>
                    </div>
                  </div>
                </div>
                </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script>
  import NavBar from '@/components/NavBar.vue'
  
  export default {
    name: 'MyProfile',
    components: {
      NavBar
    },
    data() {
      return {
        errorMessage: "",
        isLoading: true,
        user_data: {},
        currentBookings: [],
        bookingHistory: [],

        isAuthenticated: false, // Represents the user's authentication state
        selectedCity: localStorage.getItem('selectedCity') || null,
      };
    },
    methods: {
      async getProfileData() {
        const token = localStorage.getItem('access_token');
        try {
          const response = await fetch('http://127.0.0.1:5000/api/ProfileData', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          if (response.ok) {
            this.user_data = await response.json();
          } else {
            const errorText = await response.text();
            throw new Error(`Failed to fetch user data: ${response.status} - ${errorText}`);
          }
        } catch (error) {
          this.errorMessage = `An error occurred while fetching user data: ${error.message}`;
          console.error(this.errorMessage);
        }
      },
      async getCurrentBookings() {
        const token = localStorage.getItem('access_token');
        try {
          const response = await fetch('http://127.0.0.1:5000/api/CurrentBookings', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          if (response.ok) {
            // let bookings = await response.json();
            // this.currentBookings = bookings.map(booking => JSON.parse(booking));
            this.currentBookings = await response.json();
            console.log("current bookings: ", this.currentBookings)
          } else {
            const errorText = await response.text();
            throw new Error(`Failed to fetch current bookings: ${response.status} - ${errorText}`);
          }
        } catch (error) {
          this.errorMessage = `An error occurred while fetching current bookings: ${error.message}`;
          console.error(this.errorMessage);
        }
      },
      async getBookingHistory() {
        const token = localStorage.getItem('access_token');
        try {
          const response = await fetch('http://127.0.0.1:5000/api/BookingHistory', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          if (response.ok) {
            this.bookingHistory = await response.json();
            console.log(this.bookingHistory)
          } else {
            const errorText = await response.text();
            throw new Error(`Failed to fetch booking history: ${response.status} - ${errorText}`);
          }
        } catch (error) {
          this.errorMessage = `An error occurred while fetching booking history: ${error.message}`;
          console.error(this.errorMessage);
        }
      },

      formatDate(dateString) {
        return dateString.substring(0, 16);
  },
  handleEditProfile() {
    console.log('Edit profile button clicked');
    // Add your logic for handling profile editing here.
    this.$router.push('/EditProfilePage');
  },
  
    },
    async created() {
  try {
    await Promise.all([
      this.getProfileData(),
      this.getCurrentBookings(),
      this.getBookingHistory(),
    ]);
  } catch (error) {
    console.log(error);
  }
},
  }
  </script>
  
  <style scoped>
  .booking-card {
    width: 18rem;
    border: 1px solid #000;
    border-radius: 10px;
  }
  
  .booking-card-header {
    background-color: #000;
    color: #fff;
    padding: 10px;
    border-radius: 10px 10px 0 0;
  }
  
  .booking-card-body {
    padding: 10px;
  }

  .edit-profile {
  background-color: grey;
  color: white;
  border: none;
  padding: 5px 10px; /* Adjust padding to control the height and width of the button */
  margin-top: 130px;
  margin-left: 1100px;
  cursor: pointer;
  border-radius: 15px; /* This makes the corners rounded */
  font-size: 0.9em; /* Adjust font size if needed */
}

.card-item {
  margin-bottom: 18px; /* Adjust this value as needed */
  /* margin-bottom: 12px; */
  margin-top: 10px;
  font-size: 16px; /* Adjust font-size as needed */
}

#app {
  background-color: #FAF9F6;
  min-height: 100vh;
}


  </style>

