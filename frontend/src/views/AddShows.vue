
<template>
    <div class="wrapper">
    <!-- Sidebar  -->
    <nav id="sidebar">
        <div class="sidebar-header">
            <h3>BookIt</h3>
        </div>

        <ul class="list-unstyled components">
            <p>Add Shows Page</p>
            
            <li>
                <router-link to="/admin/Home">Home</router-link>
            </li>

            <li>
                <router-link to="/admin/AddTheatre">Add Theatre</router-link>
            </li>

            <li>
                <router-link to="/admin/ManageTheatres"> Manage Theatres</router-link>
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
      <div class="container">
        <div class="row">
          <!-- Display long cards for each theater -->
          <div
            class="col-lg-4 col-md-6 col-sm-12 mb-4"
            v-for="theater in theaters"
            :key="theater.theatre_id"
          >
            <div class="card">
              <div class="card-body">
                <h5 class="card-title font-weight-bold">{{ theater.theatre_name }}</h5>
                <!-- <p class="card-text">
                  <strong>City:</strong> {{ theater.city }}
                  <br>
                  <strong>Screens:</strong> {{ theater.screens }}
                  <br>
                  <strong>Address:</strong> {{ theater.address }}
                </p> -->
                <div class="card-text">
                    <div class="card-item">
                      <strong>City:</strong> {{ theater.city }}
                    </div>
                    <div class="card-item">
                      <strong>Screens:</strong> {{ theater.screens }}
                    </div>
                    <div class="card-item">
                      <strong>Address:</strong> {{ theater.address }}
                    </div>
                </div>



                <button @click="openAddShowPopup(theater.theatre_id)" class="btn btn-primary">Add Show</button>
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



    
    <!-- Add Show Form Popup -->
    <AddShowForm
      v-if="showAddShowPopup"
      :theaterId="selectedTheaterId" 
      @add-show="handleAddShow"
      @close="closeAddShowPopup"
      @cancel="cancelAddShowPopup"
    />

      </div>


</template>



<script>
import AddShowForm from '../components/AddShowPopUp.vue';

// import NavBar from '@/components/NavBar.vue' // import the Navbar component
// import CityPopup from '../components/CityPopup.vue';
  export default {
    components: {
    AddShowForm
  },
    data() {
      return {
        theaters: [],
        // errorMessage: ""
        showAddShowPopup: false, // Flag to control the visibility of the add show form popup
        selectedTheaterId: null, // ID of the theater for which the add show button was clicked
        response_message: '',
      };
    },
    methods: {
    openAddShowPopup(theaterId) {
      this.selectedTheaterId = theaterId;
      this.showAddShowPopup = true;
    },
    closeAddShowPopup() {
      this.showAddShowPopup = false;
      this.response_message = "Show added successfully"; 
    },
    cancelAddShowPopup() {
      this.showAddShowPopup = false;
    },
    handleAddShow(show) {
      // Process the added show and selected theater ID
      console.log(`Theater ID: ${this.selectedTheaterId}`);
      console.log(show);

      // Close the add show form pop-up
      this.closeAddShowPopup();
    }
  },

    mounted() {
      const token = localStorage.getItem('access_token');
      fetch('http://127.0.0.1:5000/api/TheatreData', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => response.json())
        .then(data => {
          // Handle the retrieved theater data
          this.theaters = data;
        })
        .catch(error => {
          // Handle any errors
          console.error(error);
        });
    }
  };

</script>

<style scoped>
.card-item {
  margin-bottom: 12px; /* Adjust this value as needed */
  font-size: 16px; /* Adjust font-size as needed */
}
</style>







