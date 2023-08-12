
<template>
    <div class="wrapper">
    <!-- Sidebar  -->
    <nav id="sidebar">
        <div class="sidebar-header">
            <h3>BookIt</h3>
        </div>

        <ul class="list-unstyled components">
            <p>Manage Theatres Page</p>

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
                <button  @click="editTheatre(theater.theatre_id)" class="btn btn-primary btn-sm ">Edit Theatre</button>
                <button @click="deleteTheatre(theater)" class="btn btn-danger btn-sm btn-spacing">Delete Theatre</button>
                <button @click="exportTheatreData(theater.theatre_id)" class="btn btn-info btn-sm ">Export Data</button>
             </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- <EditTheatrePopup
    v-if="showEditTheatrePopup"
    :theatre="selectedTheatre"
    @update-theatre="handleUpdateTheatre"
    @close="showEditTheatrePopup = false"
  /> -->
<!-- 
  <DeleteConfirmationPopup
    v-if="showDeleteConfirmationPopup"
    @confirm="handleDeleteTheatre"
    @cancel="showDeleteConfirmationPopup = false"
  /> -->

  </div>


</template>

<script>
import EditTheatrePopup from '../components/EditTheatrePopup.vue';
import DeleteConfirmationPopup from '../components/DeleteConfirmationPopup.vue';

export default {
  components: {
    EditTheatrePopup,
    DeleteConfirmationPopup
  },
  data() {
    return {
      theaters: [],
      selectedTheatre: null,
      showEditTheatrePopup: false,
      showDeleteConfirmationPopup: false,
    };
  },
  methods: {
    fetchTheatreData() {
      const token = localStorage.getItem('access_token');
      fetch('http://127.0.0.1:5000/api/TheatreData', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        }
      })
      .then(response => response.json())
      .then(theatres => {
        return Promise.all(
          theatres.map(theatre => 
            fetch(`http://127.0.0.1:5000/api/ShowsApi/${theatre.theatre_id}`, {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`
              }
            })
            .then(response => response.json())
            .then(shows => {
              theatre.shows = shows;
              return theatre;
            })
          )
        );
      })
      .then(theatres => {
        this.theaters = theatres;
      })
      .catch(error => {
        console.error(error);
      });
    },
    handleUpdateTheatre(updatedTheatre) {
      const index = this.theaters.findIndex(theatre => theatre.theatre_id === updatedTheatre.theatre_id);
      this.$set(this.theaters, index, updatedTheatre);
      this.showEditTheatrePopup = false;
    },
    deleteTheatre(theatre) {
      if (confirm(`Are you sure you want to delete theatre: ${theatre.theatre_name}?`)) {
        const token = localStorage.getItem('access_token');
        fetch(`http://127.0.0.1:5000/api/TheatreData/${theatre.theatre_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            this.theaters = this.theaters.filter(t => t.theatre_id !== theatre.theatre_id);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
      }
    },
    
    exportTheatreData(theatreId) {
      const token = localStorage.getItem('access_token');
      
      fetch(`http://127.0.0.1:5000/api/export_theatre_data/${theatreId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        
        return response.json();
      })
      .then(responseData => {
        alert(responseData.message);
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });
    },

    editTheatre(theatreId) {
        this.$router.push(`./EditTheatre/${theatreId}`);
    }

  },
  mounted() {
    this.fetchTheatreData();
  }
};
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

.show-card p {
  margin: 0;
}
</style>

<style scoped>
.card-item {
  margin-bottom: 15px; /* Adjust this value as needed */
  /* margin-bottom: 12px; */
  font-size: 16px; /* Adjust font-size as needed */
}

.btn-spacing {
  margin-right: 10px;
  margin-left: 10px; 
}

</style>
