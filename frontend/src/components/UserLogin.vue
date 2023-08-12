<template>
    <div class="add-show-form">
       
      <div class="modal">
        <button class="close-button" @click="$emit('close-popup')">✕</button>
        <div class="modal-content">
          <h3>Log Into BookIt Account</h3>

          <br>

          <form @submit.prevent="submitForm">
            

            <div class="form-group">
              <label for="timing">USERNAME</label>
              <br>
              <input v-model="username" type="text" id="timing"  class="form-control" required>
            </div>
            
            <br>
        
            
            <div class="form-group">
              <label for="ticketPrice">PASSWORD</label>
              <br>
              <input v-model="password" id="ticketPrice" type="password" class="form-control" required>
            </div>

            

            <br>
            <!-- @submit.prevent="submitForm" -->
            <div class="form-group">
              <button  @click="handleLogin"  class="btn btn-primary" >submit</button>
              <button @click="closePopup" type="button" class="btn btn-secondary">Cancel</button>
            </div>

            <br>
            <br>
            <p style="font-size: 0.9em;" >Already have an account? <button @click="$emit('open-sign-up')">Sign up</button> </p> <!-- Sign up link -->
            
     
          </form>
        </div>
      </div>
    </div>
  </template>
  <script>
  export default {
    name: 'UserLogin',
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      async handleLogin() {
        if (this.username && this.password) {
          let response = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              username: this.username,
              password: this.password
            })
          });
          if (response.status === 200) {
            let data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('isAuthenticated', true); // set isAuthenticated in local storage  
            this.$emit('userLoggedIn');
          } else if (response.status === 401) {
            console.error("Invalid credentials!");
          } else if (response.status === 409) {
            console.error("Username does not exist!");
          } else {
            console.error("An error occurred while logging in!");
          }
        } else {
          console.error("Invalid credentials!");
        }
      },
      closePopup() {
      this.$emit('close-popup');
    },
    },
  };
  </script>

  

<style scoped>



.add-show-form {

  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 400px;
  width: 90%;
  height: 55%;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  /* display: flex;
  align-items: center;
  justify-content: center;
  height: 100%; */
}

.modal {
  /* background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0; */

  
  display: flex;
  /* align-items: center; */
  /* justify-content: center; */
/* 
  position: fixed;
  top: 30%;
  left: 51%;
  transform: translate(-50%, -50%);
  max-width: 400px;
  height
  width: 100%;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); */
  
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
}

.close-button {
position: absolute;
top: 10px;
right: 10px;
font-size: 20px;
font-weight: bold;
color: #555;
background: transparent;
border: none;
cursor: pointer;
}

.component-root-class {
  z-index: 10000; /* Or any higher value to ensure it's above all other elements */
}
</style>
