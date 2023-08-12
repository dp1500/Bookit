
<template>

  <div id="app">
    <div class="wrapper">
    <!-- Sidebar  -->
    <nav id="sidebar">
        <div class="sidebar-header">
            <h3>BookIt</h3>
        </div>

        <ul class="list-unstyled components">
            <p>Add Theatre Page</p>

            <li>
                <router-link to="/admin/Home">Home</router-link>
            </li>

            <li>
                <router-link to="/admin/ManageTheatres"> Manage Theatres</router-link>
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
    
    <!-- Page Content  -->
    <div id="content">
        
        <h2>
            Add Theatre Details
        </h2>
        <br>
        <form @submit.prevent="sendTheatreData">
        <div class="form-row">
          <div class="form-group col-md-6">
            <!-- <label for="theatreName">Theatre Name</label> -->
            <input type="text" class="form-control" id="theatreName" v-model="theatreName" placeholder="Theatre Name" required>
          </div>

          <!-- <div class="form-group col-md-6"> -->
            <!-- <label for="capacity">Capacity</label> -->
            <!-- <input type="number"  class="form-control" id="screens" v-model="screens" placeholder="Number of Screens" required>
          </div> -->

          <div class="form-group col-md-6">
        <label for="screenCount">Screen Count:</label>
        <input class="form-control" type="number" v-model="screenCount" id="screenCount" placeholder="Number of Screens">
          </div>
        
        <div class="form-group col-md-6" v-for="index in screenCountArray" :key="index">
          <label :for="'screenCapacity-' + index">Screen {{ index }} Capacity:</label>
          <input class="form-control" :id="'screenCapacity-' + index" type="number" v-model="screenCapacities[index - 1]">
        </div>

          <div v-for="index in screens" :key="index" class="form-group col-md-6">
          <input type="number" class="form-control" :id="'screenCapacity-' + index" :placeholder="'Capacity - Screen ' + index" required>
        </div>

          <div class="form-group col-md-6">
            <label for="capacity">Total Capacity</label>
            <input  class="form-control" id="capacity" v-model="totalCapacity" placeholder="Total Capacity" required>
          </div>

        </div>
        <div class="form-group col-md-6">
          <!-- <label for="city">City</label> -->   
          <select class="form-control" id="city" v-model="city" required>
            <option value="" disabled selected>Select a city</option>
            <option value="Delhi NCR">Delhi NCR</option>
            <option value="Mumbai">Mumbai</option>
            <option value="Pune">Pune</option>
            <option value="Bengaluru">Bengaluru</option>
            <option value="Chennai">Chennai</option>
            <option value="Hyderabad">Hyderabad</option>
          </select>
        </div>

        <div class="form-group col-md-6">
            <!-- <label for="address">Capacity</label> -->
            <input  class="form-control" id="address" v-model="address" placeholder="Address" required>
        </div>

        <button type="submit" class="btn btn-primary">Add Theatre</button>
      </form>
      <div v-if="errorMessage"
              class= "alert alert-warning alert-dismissible fade show mt-2"
              role="alert">
                <strong> {{ errorMessage }} </strong>
            </div>
    
 
      </div>
    </div>
  </div>

</template>
  
<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.sidebar {
  /* Add sidebar styles */
  width: 250px; /* Adjust the width as needed */
}

.content {
  /* Add content styles */
  width: 400px; /* Adjust the width as needed */
  /* margin-left: 50%; */
}

.form-group {
  width: 100%;
  margin-bottom: 5%;
}

.form-control {
  width: 100%;
}

/* #app {
  background-color: #FAF9F6;
  min-height: 100vh;
} */

</style>

  
  
  <script>
  export default {
    data() {
      return {
        theatreName: '',
        errorMessage: "",
        city: '',
        address: '',
        // capacity: null,
        screens: null,
        
        screenCount: 0,
      screenCapacities: []
      };
    },
    

      methods: {
        sendTheatreData(){

            if(!this.theatreName || !this.totalCapacity || !this.city || !this.address){
              this.errorMessage = " Kindly add all the required fields"
            }
          
            else{
            
                console.log(this.theatreName, this.capacity, this.city, this.address, this.screens)
            const token = localStorage.getItem('access_token');
              fetch('http://127.0.0.1:5000//api/TheatreData', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify({theatreName:this.theatreName, capacity:this.totalCapacity, city:this.city, address:this.address,screens:this.screenCount,screenCapacities: this.screenCapacities,})
                })
              .then(response => {

                if (response.status === 409){
                  throw new Error("Username already in use. Please pick another username");
                }

                else if (response.status === 401){
                  throw new Error("UNAUTHORISED USER");
                }

                else if (response.ok) {
                  return response.json()
                  }
                
                // throw new Error("username already in use.Please pick another username");
                  })
              .then(() => {
                this.$router.push({
                  name:'AdminHome'
                })
              })
              .catch(error => {
                console.error('Error:', error)
                this.errorMessage = error.message

              })

            }
            
        },
        
    },

      computed: {
    screenCountArray() {
      return Array.from({ length: parseInt(this.screenCount) }, (_, index) => index + 1);
    },
    totalCapacity() {
      return this.screenCapacities.reduce((total, capacity) => total + parseInt(capacity), 0);
    },
  }
    
  };
  </script>
  
  
  