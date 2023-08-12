<template>
    <div class="modal">
    <div class="add-show-form">
      <form @submit.prevent="updateTheatreData">
        <div class="form-group">
          <input type="text" class="form-control" v-model="theatre.theatreName" placeholder="Theatre Name" required>
        </div>
        <div class="form-group">
          <input type="number" class="form-control" v-model="theatre.totalCapacity" placeholder="Total Capacity" required>
        </div>
        <div class="form-group">
          <select class="form-control" v-model="theatre.city" required>
            <option value="" disabled selected>Select a city</option>
            <option value="Delhi NCR">Delhi NCR</option>
            <option value="Mumbai">Mumbai</option>
            <option value="Pune">Pune</option>
            <!-- Add other options as necessary -->
          </select>
        </div>
        <div class="form-group">
          <input type="text" class="form-control" v-model="theatre.address" placeholder="Address" required>
        </div>
        <button type="submit" class="btn btn-primary" >Update Theatre</button>
        <!-- @click="$emit('Update-Theatre')" -->
        <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
      </form>
    </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      theatre: {
        type: Object,
        required: true
      }
    },
    methods: {
      updateTheatreData() {
        const token = localStorage.getItem('access_token');

            fetch(`http://127.0.0.1:5000/api/TheatreData/${this.theatre.theatre_id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                theatreName: this.theatre.theatreName,
                capacity: this.theatre.totalCapacity,
                city: this.theatre.city,
                address: this.theatre.address,
                screens: this.theatre.screenCount,
                screenCapacities: this.theatre.screenCapacities,
            }),
            })
            .then(response => {
                if (!response.ok) {
                throw new Error("Error updating theatre");
                }
                return response.json();
            })
            .then(updatedTheatre => {
                // Emit the updated theatre data
                this.$emit('update-theatre', updatedTheatre);
                // Close the popup
                this.$emit('close');
            })
            .catch(error => {
                console.error('Error:', error);
                // You could also emit an error event or handle the error in some other way
            });
            
        // Close the popup
        this.$emit('close');
      }
    },
    created(){
        console.log("editheatre pop up created")
        console.log("editheatre pop up created" , this.theatre)
    }
  }
  </script>
  
  <style scoped>
  .add-show-form {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    max-width: 400px;
    width: 90%;
    height: 70%;
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  }
  
  .modal {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
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
  </style>

  