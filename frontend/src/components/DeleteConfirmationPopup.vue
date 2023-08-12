<template>
    <div class="popup">
      <p>Are you sure you want to delete this theatre?</p>
      <button class="btn btn-danger" @click="$emit('confirm')">Yes, I confirm</button>
      <button class="btn btn-primary" @click="$emit('cancel')">Cancel</button>
    </div>
  </template>
  
  <script>
  export default {
    // No data or methods needed for this component
  }
  </script>
  
  <style scoped>
    /* Add your styles here */
  </style>
  