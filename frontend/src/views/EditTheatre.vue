<template>
    <div class="wrapper">
        <!-- Sidebar  -->
    <nav id="sidebar">
        <div class="sidebar-header">
            <h3>BookIt</h3>
        </div>

        <ul class="list-unstyled components">
            <p>Edit Theatre Page</p>
            
            <li>
                <router-link to="/admin/Home">Home</router-link>
            </li>

            <li>
                <router-link to="/admin/AddTheatre">Add Theatre</router-link>
            </li>

            <li>
                <router-link to="/admin/AddShows">Add Shows</router-link>
            </li>

            <li>
                <router-link to="/admin/manageShows">Manage Shows</router-link>
            </li>

            <li>
                <router-link to="/admin/AddMovie">Add Movie</router-link>
            </li>
        </ul>
    </nav>

    <!-- <div class="add-show-form"> -->
        <div id="content">
        <form @submit.prevent="updateTheatreData">
            <div class="form-group">
        <label for="theatreName">Theatre Name</label>
        <input type="text" class="form-control" v-model="theatre.theatre_name" id="theatreName" placeholder="Theatre Name" required>
      </div>
      
   <br>
   
    
  <div class="form-group">
    <label for="city">City</label>
    <select class="form-control" v-model="theatre.city" required>
      <option value="" disabled selected>Select a city</option>
      <option value="Delhi NCR">Delhi NCR</option>
      <option value="Mumbai">Mumbai</option>
      <option value="Pune">Pune</option>
      <option value="Bangalore">Bangalore</option> 
      <option value="Chennai">Chennai</option>
      <option value="Hyderabad">Hyderabad</option>
      <!-- Add other options as necessary -->
    </select>

    <br>
    <br>

  </div>
  <div class="form-group">
    <input type="text" class="form-control" v-model="theatre.address" placeholder="Address" required>
  </div>

  <br>

  <div class="form-group">
        <label for="screenCount">Screen Count</label>
        <input class="form-control" type="number" v-model="screenCount" id="screenCount" placeholder="Number of Screens" required min="1">
      </div>

      <br>
      <br>

      <div class="form-group" v-for="index in screenCountArray" :key="index">
        <label :for="'screenCapacity-' + index">Screen {{ index }} Capacity</label>
        <input class="form-control" :id="'screenCapacity-' + index" type="numeric" v-model="screenCapacities[index - 1]" required min="1">
      </div>
    
        <br>

    <!-- <div class="form-group">
    <input type="number" class="form-control" v-model="theatre.capacity" placeholder="Total Capacity" required>
  </div> -->

  <!-- <div class="form-group col-md-6">
            <label for="capacity">Total Capacity</label>
            <input  class="form-control" id="capacity" v-model="theatre.capacity" placeholder="Total Capacity" required>
          </div> -->
        
          <div class="form-group col-md-6">
            <label for="capacity">Total Capacity</label>
            <p class="form-control-static">{{ totalCapacity }}</p>
            </div>

  <button type="submit" class="btn btn-primary" >Update Theatre</button>
  <!-- @click="$emit('Update-Theatre')" -->
  
</form>

<div v-if="response_message"
              class= "alert alert-warning alert-dismissible fade show mt-2"
              role="alert">
                <strong> {{ response_message }} </strong>
        </div>
    </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        theatre: null,
      errorMessage: "",
      screenCount: 0,
      screenCapacities: [],
      response_message: '',
      };
    },
    mounted() {
    const theatreId = this.$route.params.theatre_id;
    const token = localStorage.getItem('access_token');

    const headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    };

    const fetchTheatreData = fetch(`http://127.0.0.1:5000/api/TheatreData/${theatreId}`, {
      method: 'GET',
      headers: headers
    })
      .then(response => response.json());

    const fetchScreenData = fetchTheatreData
      .then(data => {
        this.theatre = data;
        this.screenCount = this.theatre.screens;
        this.screenCapacities = [];  // Initialize screenCapacities as an empty array

        return fetch(`http://127.0.0.1:5000/api/ScreensApi/${theatreId}`, {
          method: 'GET',
          headers: headers
        });
      })
      .then(response => response.json());

    Promise.all([fetchTheatreData, fetchScreenData])
      .then(([theatre, screenData]) => {
        screenData.forEach((screen, index) => {
          this.$set(this.screenCapacities, index, screen.screen_capacity);  // Use Vue.set() to ensure reactivity
        });
      })
      .catch(error => {
        console.error(error);
      });
}
,
    methods: {
    updateTheatreData() {
      if(!this.theatre || this.screenCapacities.includes(null)) {
        this.errorMessage = "Kindly add all the required fields";
        return;
      }

      const token = localStorage.getItem('access_token');
      fetch(`http://127.0.0.1:5000/api/TheatreData/${this.theatre.theatre_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          theatreName: this.theatre.theatre_name,
        //   capacity: this.theatre.capacity,
            capacity: this.totalCapacity,
          city: this.theatre.city,
          address: this.theatre.address,
          screens: this.screenCount,
          screenCapacities: this.screenCapacities,
        })
      })
        .then(response => {
          if(!response.ok) {
            throw new Error("An error occurred while updating theatre data");
          }
          return response.json();
        })
        .then(() => {
          this.$router.push({ name: 'AdminHome' });
        })
        .catch(error => {
          console.error('Error:', error);
          this.errorMessage = error.message;
        });
    },
  },
  computed: {
    screenCountArray() {
      return Array.from({ length: this.screenCount }, (_, index) => index + 1);
    },
    totalCapacity() {
      return this.screenCapacities.reduce((total, capacity) => total + parseInt(capacity || 0), 0);
    },
  },

  watch: {
    screenCount(newValue, oldValue) {
      // Add new screen capacity inputs if the screen count increases
      for(let i = oldValue; i < newValue; i++) {
        this.screenCapacities.push(0);
      }

      // Remove screen capacity inputs if the screen count decreases
      this.screenCapacities = this.screenCapacities.slice(0, newValue);
    }
  },

    
  };
  </script>


<style scoped>
.add-show-form {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.form-group {
  width: 100%;
  margin-bottom: 0px;
}

.form-group input,
.form-group select {
  width: 100%;
}

button {
  margin-top: 10px;
}
</style>
