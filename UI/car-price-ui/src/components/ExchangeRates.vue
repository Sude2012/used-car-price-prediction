<template>
  <div>
    <h2>Döviz Kurları</h2>

    <div v-if="error" style="color:red">
      Hata: {{ error }}
    </div>

    <ul v-if="rates">
      <li v-for="(rate, currency) in rates" :key="currency">
        {{ currency }} : {{ rate }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      rates: null,
      error: null,
    };
  },

  async mounted() {
    try {
      const res = await fetch("http://localhost:4000/api/exchange");
      this.rates = (await res.json()).rates;
    } catch (e) {
      this.error = "API'ye ulaşılamadı!";
    }
  },
};
</script>

