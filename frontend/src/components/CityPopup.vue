<template>
  <div class="city-popup">
    <button class="close-button" @click="$emit('closePopup')">✕</button>
    <h2>Select Your City</h2>
    <div class="city-list">
      <div v-for="city in cities" :key="city.name" class="city" @click="selectCity(city.name)">
        <img :src="city.image" :alt="city.name" class="city-image" />
        <p class="city-name">{{ city.name }}</p>
      </div>
    </div>
  </div>
</template>

<script> 
export default {
  data() {
    return {
      cities: [
        { name: 'Delhi NCR', image: 'delhi-ncr.jpg' },
        { name: 'Mumbai', image: 'mumbai.jpg' },
        { name: 'Bangalore', image: 'bangalore.jpg' },
        { name: 'Chennai', image: 'Chennai.jpg' },
        { name: 'Pune', image: 'pune.jpg' },
        { name: 'Hyderabad', image: 'Hyderabad.jpg' },
      ],
    };
  },
  methods: {
  selectCity(city) {

    localStorage.removeItem('selectedCity');

    // Store the selected city in localStorage
    localStorage.setItem('selectedCity', city);
    console.log(city)
    // Emit an event to close the popup
    // this.$router.go(0); // Reload the current page 
    this.$emit('closePopup');
    
  },
},
};



</script>

<style scoped>
.city-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 400px;
  width: 90%;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
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

h2 {
  margin-top: 0;
  text-align: center;
}

.city-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-gap: 10px;
  margin-top: 20px;
}

.city {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  border-radius: 10px;
  background-color: #f0f0f0;
  cursor: pointer;
}

.city-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 10px;
}

.city-name {
  margin-top: 5px;
  font-weight: bold;
  text-align: center;
}
</style>
