<template>
    <body>
   
<!-- jinja template  {% with messages = get_flashed_messages() %}
        {% if messages %} -->
    
            <!-- <div class="alert alert-primary" role="alert">
                    {{ messages|last }} 
                    
            </div> -->

        <!-- {% endif %}
    {% endwith %} -->

<section class="vh-100 bg-image"
style="background-image: url('/krists-luhaers-AtPWnYNDJnM-unsplash.jpg'); background-size: 100% 100%; background-position: center; background-repeat: no-repeat; width: 100%; height: 200%;">


<!-- style="background-image: url('https://mdbcdn.b-cdn.net/img/Photos/new-templates/search-box/img4.webp');" -->

<div class="mask d-flex align-items-center h-100 gradient-custom-3">
<div class="container h-100">
  <div class="row d-flex justify-content-center align-items-center h-100">
    <div class="col-12 col-md-9 col-lg-7 col-xl-6">
      <div class="card" style="border-radius: 15px;">
        <div class="card-body p-3">
          <h2 class="text-uppercase text-center mb-5">Create an admin account</h2>

          <form @submit.prevent="sendUserSignUpDataRoleAdmin" >

            <div class="form-outline mb-2">
              <input type="text" id="name" name="name" class="form-control form-control-lg" v-model="name"/>
              <label class="form-label" for="name">Your Name</label>
            </div>

            <div class="form-outline mb-2">
              <input type="text" id="username" name="username" class="form-control form-control-lg" v-model="username"/>
              <label class="form-label" for="username">Enter a username</label>
            </div>

            <div class="form-outline mb-2">
              <input type="email" id="email" name="email" class="form-control form-control-lg" v-model="email"/>
              <label class="form-label" for="email">Enter Your Email ID</label>
            </div>

            <div class="form-outline mb-2">
              <input type="password" id="password" name="password" class="form-control form-control-lg" v-model="password"/>
              <label class="form-label" for="password">Password</label>
            </div>

            <div class="form-outline mb-2">
              <input type="password" id="repeat_password" name="repeat_password" class="form-control form-control-lg" v-model="repeat_password"/>
              <label class="form-label" for="repeat_password">Repeat your password</label>
            </div>

            <div class="d-flex justify-content-center">
              <button type="submit"
                class="btn btn-primary btn-lg">Register</button>
            </div>

            <p class="text-center text-muted mt-3 mb-0">Already have an account? <a href='/admin'
                class="fw-bold text-body" style="font-size:18px; color: blue;"><u>Login here</u></a></p>

          </form>

            <div v-if="errorMessage"
              class= "alert alert-warning alert-dismissible fade show mt-2"
              role="alert">
                <strong> {{ errorMessage }} </strong>
            </div>

        </div>
      </div>
    </div>
  </div>
</div>
</div>
</section>
 
</body>
  </template>

<script>
// import axios from 'axios';
export default {
    name:'SignUp',
    data() {
        return {
            errorMessage: "",
            name: null,
            username: null,
            email: null,
            password: null,
            repeat_password: null,
        };
    },
    methods: {
        sendUserSignUpDataRoleAdmin(){

            if(!this.name || !this.username || !this.email || !this.password || !this.repeat_password){
              this.errorMessage = " Kindly add all the required fields"
            }

            else if(this.password != this.repeat_password){
              this.errorMessage = " passwords do not match"
            }

            
            
            else{

              fetch('http://127.0.0.1:5000/api/ProfileData', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({name:this.name, username:this.username, email:this.email, password:this.password, repeat_password:this.repeat_password,role:'admin' })
                })
              .then(response => {

                if (response.status === 409){
                  throw new Error("Username already in use. Please pick another username");
                }

                else if (response.ok) {
                  return response.json()
                  }
                
                // throw new Error("username already in use.Please pick another username");
                  })
              .then(() => {
                this.$router.push({
                  name:'AdminLogin'
                })
              })
              .catch(error => {
                console.error('Error:', error)
                this.errorMessage = error.message

              })

            }
            
        },
    },

    created(){
        // this.sendUserSignUpData()
    }
}
</script>


