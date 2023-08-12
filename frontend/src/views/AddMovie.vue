
<template>
    <div class="wrapper">
    <!-- Sidebar  -->
    <nav id="sidebar">
        <div class="sidebar-header">
            <h3>BookIt</h3>
        </div>

        <ul class="list-unstyled components">
            <p>Add Movie Page</p>

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
                <router-link to="/admin/AddShows">Add Shows</router-link>
            </li>

            <li>
                <router-link to="/admin/manageShows">Manage Shows</router-link>
            </li>
           
        </ul>
    </nav>

    <!-- Page Content  -->
    <div id="content">
        
        <h2>
            Add Movie Details
        </h2>
        <br>
        <form accept-charset="UTF-8" enctype="multipart/form-data" @submit.prevent="sendNewMovieData">
  <div class="form-group" >
    <!-- <label for="title" >Movie Name</label> -->
    <input type="text" name="title" class="form-control" id="title" placeholder="Movie Name" v-model="title" required>
  </div>
  <br>
 
  <div class="form-group">
   <!-- <label for="description">Movie Description</label> -->
    <textarea id="description" name="description" rows="3" cols="152" v-model="description" placeholder="Movie Description"></textarea>
  </div>
  <br>

        <div class="form-group" >
            <!-- <label for="title" >Movie Name</label> -->
            <input type="text" class="form-control" id="date" placeholder="dd month yyyy" v-model="releaseDate" required>
        </div>
        <br>
    
        <div class="form-group">
            <input type="number" name="rating" class="form-control" id="rating" placeholder="Movie Rating" v-model="rating" min="1" max="10" required>
        </div>

  <!-- <div class="form-group">
              <label for="date">Date</label>
              <input v-model="releaseDate" type="date" id="date" class="form-control" required>
            </div>
  <br> -->

    <div class="form-group">
    <label>Genres</label><br>
    <div class="form-check form-check-inline" v-for="genre in genreOptions" :key="genre">
        <input class="form-check-input" type="checkbox" :value="genre" v-model="selectedGenres">
        <label class="form-check-label">{{ genre }}</label>
    </div>
    </div>
  
  <hr>
  <div class="form-group mt-3">
    <label class="mr-2">Upload Image:</label>
    <input type="file" name="file" @change="onFileSelected">
  </div>
  <hr>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>

      <div v-if="errorMessage"
              class= "alert alert-warning alert-dismissible fade show mt-2"
              role="alert">
                <strong> {{ errorMessage }} </strong>
            </div>

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
  name: 'AddMovie',

  data() {
        return {
            errorMessage: "",
            response_message: "",
            title: null,
            description: null,
            releaseDate: null,
            selectedGenres: [],
            imageFile:null,
            rating: null,
            genreOptions: [
            'Action', 'Drama', 'Adventure', 'Fiction', 'Sci-Fi',
            'History', 'Documentary', 'Romance', 'Comedy', 'Horror'
            ],
        };
    },

    methods: {

        onFileSelected(event) {
            console.log(event)
            this.imageFile = event.target.files[0];
            },


        sendNewMovieData(){
                

                if(!this.title || !this.description || !this.releaseDate || !this.selectedGenres ){
              this.errorMessage = " Kindly add all the required fields"
                }

                else if(!this.imageFile ){
                    this.errorMessage = " Kindly also add an image file"
                  }

              
                
                else{
                    const formData = new FormData();

                    const genresString = this.selectedGenres.length > 0 ? this.selectedGenres.join(', ') : '';
                    formData.append('genres', genresString);
                    formData.append('file', this.imageFile);
                    formData.append('title', this.title);
                    formData.append('description', this.description);
                    formData.append('releaseDate', this.releaseDate);
                    formData.append('rating', this.rating);
                    // formData.append('genres', genresString);
                    
              const token = localStorage.getItem('access_token');
              fetch('http://127.0.0.1:5000//api/MoviesData', {
              method: 'POST',
              headers: {
                Authorization: `Bearer ${token}`,
              },
              body: formData })
              .then(response => {

                if (response.status === 409){
                  throw new Error("file could not be uploaded");
                }

                else if (response.ok) {
                  this.response_message = "Movie added Succesfully"
                  this.errorMessage =""
                  setTimeout(() => {
                    this.$router.push({
                        name:'AdminHome'
                    });
                    }, 3000);
                //   return response.json()
                  
                  }
                })
                // maybe create a time out function here 
            //   .then(() => {
            //     this.$router.push({
            //       name:'MyProfilePage'
            //     })
            //   })
              .catch(error => {
                console.error('Error:', error)
                this.errorMessage = error.message

              })


                }
                
              }
          

            

            
            // else{
                
            // const formData = new FormData();
            // formData.append('file', this.imageFile);
            // formData.append('csvFlag', "null");
            // formData.append('title', this.title);
            // formData.append('description', this.description);
            
            // const token = localStorage.getItem('access_token');
            //   fetch('http://127.0.0.1:5000//api/BlogData', {
            //   method: 'POST',
            //   headers: {
            //     Authorization: `Bearer ${token}`,
            //   },
            //   body: formData })
            //   .then(response => {

            //     if (response.status === 409){
            //       throw new Error("file could not be uploaded");
            //     }

            //     else if (response.ok) {
            //       this.response_message = "Blog Posted Succesfully"
            //       this.errorMessage =""
            //       return response.json()
            //       }
            //     })
            //     // maybe create a time out function here 
            // //   .then(() => {
            // //     this.$router.push({
            // //       name:'MyProfilePage'
            // //     })
            // //   })
            //   .catch(error => {
            //     console.error('Error:', error)
            //     this.errorMessage = error.message

            //   })

            // }
            
        },
    

}
</script>