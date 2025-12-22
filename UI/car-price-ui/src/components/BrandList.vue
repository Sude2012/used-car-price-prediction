<template>
  <div>
    <h2>Brands</h2>

    <p>Debug: {{ brands }}</p>

    <ul v-if="brands.length > 0">
      <li v-for="b in brands" :key="b">{{ b }}</li>
    </ul>

    <p v-else>Loading or no data...</p>
  </div>
</template>

<script>
export default {
  data() {
    return { brands: [] }
  },
  async mounted() {
    try {
      console.log("Fetching brands...");

      
      const res = await fetch("https://localhost:7188/api/car/brands");


const data = await res.json();
this.brands = data;

    

    } catch (err) {
      console.error("Hata:", err);
    }
  }
}
</script>
