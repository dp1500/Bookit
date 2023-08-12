<template>

    <body>
      <br>
      <br>
      <div class = 'container'>
  
          <section class="vh-100">
              <div class="container-fluid h-custom">
                <div class="row d-flex justify-content-center align-items-center h-100">
                  <div class="col-md-9 col-lg-6 col-xl-5">
                    <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp"
                      class="img-fluid" alt="Sample image">
                  </div>
                  <div class="col-md-8 col-lg-6 col-xl-4 offset-xl-1">
                    <form @submit.prevent="login">
                      <div class="d-flex flex-row align-items-center justify-content-center justify-content-lg-start">
  
                        <p class="lead fw-normal mb-0 me-3" style="font-size:32px; color: secondary;">Welcome To Bookit Admin</p>
                        
                      </div>
                      <div class="d-flex flex-row align-items-center justify-content-center justify-content-lg-start">
                          <p class="lead fw-normal mb-0 me-3" style="font-size:20px; color: secondary;">Login to Your admin bookit account</p>
                        </div>
            
                      <div class="divider d-flex align-items-center my-4">
                        <p class="text-center fw-bold mx-3 mb-0"></p>
                      </div>
            
                      <!-- username input -->
                      <div class="form-outline mb-4">
                        <input type="text" id="username" name="username" class="form-control form-control-lg"
                          placeholder="Enter your username" v-model="username" />
                        <label class="form-label" for="username"></label>
                      </div>
            
                      <!-- Password input -->
                      <div class="form-outline mb-3">
                        <input type="password" id="password" name="password" class="form-control form-control-lg"
                          placeholder="Enter password" v-model="password"/>
                        <label class="form-label" for="password"></label>
                      </div>
            
                      <div class="d-flex justify-content-between align-items-center">
                        <!-- Checkbox
                        <div class="form-check mb-0">
                          <input class="form-check-input me-2" type="checkbox" value="" id="form2Example3" />
                          <label class="form-check-label" for="form2Example3">
                            
                          </label>
                        </div>
                        <a href="#!" class="text-body">Forgot password?</a> -->
                      </div>
            
                      <div class="text-center text-lg-start mt-4 pt-2">
                        <button type="submit" class="btn btn-primary btn-lg"
                          style="padding-left: 2.5rem; padding-right: 2.5rem;">Login</button>
                        <p class="small fw-bold mt-2 pt-1 mb-0">Don't have an account? <a href="/admin/signup"
                            class="link-danger">Register</a></p>
                      </div>
            
                    </form>
                  </div>
                        <div v-if="errorMessage"
                            class= "alert alert-warning alert-dismissible fade show mt-2"
                            role="alert">
                            <strong> {{ errorMessage }} </strong>
                        </div>
                </div>
              </div>
              
            </section>
  
      </div>
  
  
    </body>
  
  </template>
  
  <style>
  .bd-placeholder-img {
    font-size: 1.125rem;
    text-anchor: middle;
    -webkit-user-select: none;
    -moz-user-select: none;
    user-select: none;
  }
  
  @media (min-width: 768px) {
    .bd-placeholder-img-lg {
      font-size: 3.5rem;
    }
  }
  
  .b-example-divider {
    height: 3rem;
    background-color: rgba(0, 0, 0, .1);
    border: solid rgba(0, 0, 0, .15);
    border-width: 1px 0;
    box-shadow: inset 0 .5em 1.5em rgba(0, 0, 0, .1), inset 0 .125em .5em rgba(0, 0, 0, .15);
  }
  
  .b-example-vr {
    flex-shrink: 0;
    width: 1.5rem;
    height: 100vh;
  }
  
  .bi {
    vertical-align: -.125em;
    fill: currentColor;
  }
  
  .nav-scroller {
    position: relative;
    z-index: 2;
    height: 2.75rem;
    overflow-y: hidden;
  }
  
  .nav-scroller .nav {
    display: flex;
    flex-wrap: nowrap;
    padding-bottom: 1rem;
    margin-top: -1px;
    overflow-x: auto;
    text-align: center;
    white-space: nowrap;
    -webkit-overflow-scrolling: touch;
  }
  
  footer {
  /* position: fixed; */
  /* height: 50px; */
  margin-top: auto;
  /* margin-bottom: 5mm; */
  /* bottom: 0; */
  /* width: 100%; */
  text-align: center;
  margin-left: auto;
  margin-right: auto;
  }    
  </style>
  
  
  <script>
  
  // import axios from 'axios';
  export default {
      
      name:'Login_Home',
      data() {
          return {
              errorMessage: "",
              username: null,
              password: null
          };
      },
  
      methods: {
      async login() {
        if(!this.username || !this.password ){
                this.errorMessage = " Kindly add all the required fields"
              }
  
        else{
  
          try {
          const response = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              username: this.username,
              password: this.password,
            }),
          });
  
          /////handling validation from backend///
          // if all ok
          if (response.status === 200){
          const { access_token } = await response.json();
          localStorage.setItem('access_token', access_token);
          console.log("acces token is: " + localStorage.getItem('access_token'))
  
          // Redirect to feed
          this.$router.push({
                            name:'AdminHome'
                            })
            }
        
          else if (response.status === 401) {
            this.errorMessage = 'Invalid credentials';
            }
          else if (response.status === 409) {
            this.errorMessage = 'Username does not exist';
            }
  
          } catch (error) {
            console.error(error);
            // Display error message
          }
  
        }
        
      },
    },
      
  }
  
  </script>