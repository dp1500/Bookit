<template>
    <div class="wrapper">
      <!-- Sidebar -->
      <nav id="sidebar">
        <div class="sidebar-header">
            <h3>BookIt</h3>
        </div>

        <ul class="list-unstyled components">
            <p>Manage Shows Page</p>
            <li>
                <router-link to="/admin/Home">Home</router-link>
            </li>

            <li>
                <router-link to="/admin/AddTheatre">Add Theatre</router-link>
            </li>

            <li>
                <router-link to="/admin/manageTheatres">Manage Theatres</router-link>
            </li>

            <li>
                <router-link to="/admin/AddShows">Add Shows</router-link>
            </li>


            <li>
                <router-link to="/admin/AddMovie">Add Movie</router-link>
            </li>

          </ul>

        
    
      </nav>
  
      <div id="content">
        
        <div class="container" v-if="loaded">
          <!-- Loop through each theatre -->
          <div v-for="theatre in theatres" :key="theatre.theatre_id" class="mt-4">
            <h4 class="ml-3">{{ theatre.theatre_name }}</h4>
            <h5 class="ml-3">{{ theatre.address }}</h5>
            
            <table class="table">
        <thead>
          <tr>
            <th>Movie Name</th>
            <th>Date</th>
            <th>Timing</th>
            <th>Ticket Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="show in theatre.shows" :key="show.show_id">
            <td>{{ show.movie_name }}</td>
            <td>{{ show.date }}</td>
            <td>{{ show.timing }}</td>
            <td>{{ show.ticket_price }}</td>
            <td>
              <button @click="editShow(show.show_id, theatre.theatre_id)" class="btn btn-primary">Edit</button>
              <button @click="deleteShow(show.show_id)" class="btn btn-danger">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <hr>
    </div>
  </div>
  </div>
    </div>
</template>
  
  <script>
  // import AddShowForm from '../components/AddShowPopUp.vue';
  // import EditShowForm from '../components/EditShowForm.vue';
  
  export default {
    // components: {
    //   AddShowForm,
    //   EditShowForm,
    // },
    data() {
      return {
        theatres: [],
        showAddShowPopup: false,
        selectedTheatreId: null,
        showEditShowPopup: false,
        selectedShowId: null,
        loaded: false,
      };
    },
    methods: {
      openAddShowPopup(theatreId) {
        this.selectedTheatreId = theatreId;
        this.showAddShowPopup = true;
      },
      closeAddShowPopup() {
        this.showAddShowPopup = false;
      },
      handleAddShow(show) {
        // Process the added show and selected theatre ID
        console.log(`Theatre ID: ${this.selectedTheatreId}`);
        console.log(show);
  
        // Close the add show form pop-up
        this.closeAddShowPopup();
      },
      // editShow(showId) {
      //   this.selectedShowId = showId;
      //   this.showEditShowPopup = true;
      // },
      closeEditShowPopup() {
        this.showEditShowPopup = false;
      },
      handleUpdateShow(updatedShow) {
        // Process the updated show and selected show ID
        console.log(`Show ID: ${this.selectedShowId}`);
        console.log(updatedShow);
  
        // Close the edit show form pop-up
        this.closeEditShowPopup();
      },
      deleteShow(showId) {
  // Show a confirmation dialog to the user
  if (window.confirm('Are you sure you want to delete this show?')) {
    const token = localStorage.getItem('access_token');
    fetch(`http://127.0.0.1:5000/api/EditShow/${showId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    })
    .then(response => response.json())
    .then(data => {
      // If the deletion was successful, remove the show from the local state
      if (data.message === 'Show deleted successfully') {
        this.theatres = this.theatres.map(theatre => {
          theatre.shows = theatre.shows.filter(show => show.show_id !== showId);
          return theatre;
        });
        window.alert('Show deleted successfully');
      }
    })
    .catch(error => {
      console.error(error);
    });
  }
},

      editShow(showId, theatreId) {
          this.$router.push({ name: 'EditShow', params: { showId: showId, theatreId: theatreId }});
        },

    },

    beforeCreate() {const token = localStorage.getItem('access_token');

fetch('http://127.0.0.1:5000/api/TheatreData', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  },
})
  .then((response) => response.json())
  .then((theatres) => {
    // Fetch the associated shows for each theatre and return Promise objects
    const theatrePromises = theatres.map((theatre) =>
      fetch(`http://127.0.0.1:5000/api/ShowsApi/${theatre.theatre_id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => response.json())
        .then((shows) => {
          // Fetch the show details for each show and return Promise objects
          const showPromises = shows.map((show) =>
            fetch(`http://127.0.0.1:5000/api/ShowDetailsApi/${show.show_id}`, {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
              },
            })
              .then((response) => response.json())
              .then((showDetails) => {
                show.movie_name = showDetails.movie_name;
                show.date = showDetails.date;
                show.timing = showDetails.timing;
                show.ticket_price = showDetails.ticket_price;
                return show; // Return the updated show object
              })
          );

          // Wait for all show details to be fetched
          return Promise.all(showPromises)
            .then((shows) => {
              theatre.shows = shows; // Assign the updated shows to the theatre
              return theatre; // Return the updated theatre object
            });
        })
    );

    // Wait for all theatres and shows to be fetched
    Promise.all(theatrePromises)
      .then((theatres) => {
        this.theatres = theatres; // Assign the updated theatres to the data property
        this.loaded = true;
      });
  })
  .catch((error) => {
    // Handle any errors
    console.error(error);
    this.loaded = true;
  });

    
},
watch: {
  theatres: {
    handler: function (newVal) {
      console.log(newVal); // Check the value of this.theatres to see if it contains the shows data
    },
    deep: true,
  },
},
  }
  </script>
  
  

  <style scoped>
.table {
  width: 100%;
  margin-top: 1em;
  border-collapse: collapse;
}

.table th, .table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.table th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #4CAF50;
  color: white;
}
</style>
