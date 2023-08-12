<template>
    <div class="add-show-form">
      <div class="modal">
        <button class="close-button" @click="closePopup">✕</button>
        <div class="modal-content">
          <h3>Create Your BookIt Account</h3>
          <br>
          <form @submit.prevent="submitForm">
            <div class="form-group">
              <label for="name">NAME</label>
              <br>
              <input v-model="name" type="text" id="name" class="form-control" required>
            </div>
            <br>
            <div class="form-group">
              <label for="username">USERNAME</label>
              <br>
              <input v-model="username" type="text" id="username" class="form-control" required>
            </div>
            <br>
            <div class="form-group">
              <label for="email">EMAIL</label>
              <br>
              <input v-model="email" type="email" id="email" class="form-control" required>
            </div>
            <br>
            <div class="form-group">
              <label for="password">PASSWORD</label>
              <br>
              <input v-model="password" id="password" type="password" class="form-control" required>
            </div>
            <br>
            <div class="form-group">
              <label for="repeatPassword">REPEAT PASSWORD</label>
              <br>
              <input v-model="repeat_password" id="repeatPassword" type="password" class="form-control" required>
            </div>
            <br>
            <div class="form-group">
              <button @click="handleSignUp" class="btn btn-primary">Sign Up</button>
              <button @click="closePopup" type="button" class="btn btn-secondary">Cancel</button>
            </div>
            <br>
            <br>
            <p style="font-size: 0.9em;" >Already have an account? <button @click="$emit('open-login')">Log In</button></p> <!-- Log in link -->
            
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'UserSignUp',
    data() {
      return {
        name: '',
        username: '',
        email: '',
        password: '',
        repeat_password: '',
        role: 'user', // This should be set in the frontend since it is sent from the user signup form
        errorMessage: ''
      };
    },
    methods: {
      closePopup() {
        this.$emit('close-popup');
      },
      async handleSignUp() {
        if(!this.name || !this.username || !this.email || !this.password || !this.repeat_password){
          this.errorMessage = "Kindly fill in all the required fields";
        }
        else if(this.password !== this.repeat_password){
          this.errorMessage = "Passwords do not match";
        }
        else {
          const user = {
            name: this.name,
            username: this.username,
            email: this.email,
            password: this.password,
            role: this.role,
          };
  
          const response = await fetch('http://127.0.0.1:5000/api/ProfileData', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(user),
          });
  
          if (!response.ok) {
            const message = `An error has occurred: ${response.status}`;
            throw new Error(message);
          }
  
          const data = await response.json();
          this.$emit('userSignedUp', data);
        }
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
  


