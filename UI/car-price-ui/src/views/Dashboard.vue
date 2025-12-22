<template>
  <div class="min-h-screen relative overflow-hidden flex flex-col items-center gap-8 px-4 py-10">
    <!-- Gradient background -->
    <div class="absolute inset-0 bg-gradient-to-br from-slate-950 via-indigo-950 to-fuchsia-950"></div>

    <!-- Soft blobs -->
    <div class="absolute -top-24 -left-24 h-72 w-72 rounded-full bg-fuchsia-500/25 blur-3xl"></div>
    <div class="absolute top-1/3 -right-24 h-80 w-80 rounded-full bg-indigo-500/25 blur-3xl"></div>
    <div class="absolute bottom-0 left-1/3 h-72 w-72 rounded-full bg-cyan-400/15 blur-3xl"></div>

    <!-- Header mini -->
    <div class="relative w-full max-w-5xl text-center">
      <h1 class="text-3xl sm:text-4xl font-bold text-white tracking-tight">
        🚗 İkinci El Araç Fiyat Tahmini
      </h1>
      <p class="text-white/70 mt-2">
        Yapay zeka destekli model ile tahmini piyasa değerini öğrenin
      </p>
    </div>

    <!-- ⛽ Yakıt Kartları (ÜSTTE) -->
    <div class="relative w-full max-w-5xl">
      <div class="flex items-center justify-between mb-4 px-1">
        <h2 class="text-lg font-semibold text-white/90">⛽ Güncel Yakıt Fiyatları</h2>
        <span class="text-xs text-white/50">Litre (₺)</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        <div
          v-for="fuel in fuels"
          :key="fuel.name"
          class="rounded-3xl border border-white/10 bg-white/10 shadow-xl backdrop-blur-xl
                 px-5 py-5 flex items-center justify-between
                 hover:bg-white/15 transition"
        >
          <!-- Sol -->
          <div class="flex items-center gap-3">
            <div class="h-12 w-12 rounded-2xl bg-white/10 border border-white/10 flex items-center justify-center text-2xl">
              {{ fuel.icon }}
            </div>

            <div>
              <h3 class="text-sm font-semibold text-white/90">
                {{ fuel.name }}
              </h3>
              <p class="text-xs text-white/50">Litre</p>
            </div>
          </div>

          <!-- Sağ -->
          <div class="text-xl font-bold text-white">
            {{ fuel.price }} <span class="text-white/70">₺</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ANA KART -->
    <div class="relative w-full max-w-2xl">
      <div class="rounded-3xl border border-white/10 bg-white/10 shadow-2xl backdrop-blur-xl">
        <div class="p-8 sm:p-10 text-center">
          <div class="flex items-center justify-center gap-3 mb-2">
            <div class="h-11 w-11 rounded-2xl bg-white/10 border border-white/10 flex items-center justify-center">
              <span class="text-lg">📊</span>
            </div>
            <h2 class="text-2xl font-bold text-white tracking-tight">Kontrol Paneli</h2>
          </div>

          <p class="text-white/70 mb-6">
            Yeni tahmin yapabilir veya geçmiş tahminlerini görüntüleyebilirsin.
          </p>

          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link
              to="/predict"
              class="inline-flex items-center justify-center gap-2 rounded-2xl
                     bg-gradient-to-r from-fuchsia-500 to-indigo-500
                     px-8 py-4 text-lg font-semibold text-white
                     shadow-lg shadow-fuchsia-500/20
                     hover:brightness-110 active:brightness-95 transition"
            >
              🚘 Yeni Tahmin Yap
            </router-link>

            <router-link
              to="/history"
              class="inline-flex items-center justify-center gap-2 rounded-2xl
                     bg-white/10 border border-white/10
                     px-8 py-4 text-lg font-semibold text-white
                     hover:bg-white/15 transition"
            >
              📜 Geçmiş Tahminlerim
            </router-link>
          </div>

          <button
            @click="logout"
            class="mt-7 text-sm text-rose-200 hover:text-rose-100 transition underline underline-offset-4"
          >
            🚪 Çıkış Yap
          </button>

          <div class="mt-6 flex items-center gap-3">
            <div class="h-px flex-1 bg-white/10"></div>
            <span class="text-xs text-white/40">Güvenli oturum</span>
            <div class="h-px flex-1 bg-white/10"></div>
          </div>

          <p class="mt-3 text-xs text-white/45 leading-relaxed">
            Ortak bilgisayar kullanıyorsan çıkış yapmayı unutma.
          </p>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "Dashboard",

  data() {
    return {
      userId: null,
      fuels: []
    };
  },

  async mounted() {
    const id = localStorage.getItem("userId");

    if (!id) {
      this.$router.push("/login");
      return;
    }

    this.userId = id;

    try {
      const res = await fetch("http://localhost:4000/api/fuel");
      const data = await res.json();

      this.fuels = [
        { name: "Benzin", price: data.result[0].gasoline, icon: "⛽" },
        { name: "Motorin", price: data.result[0].diesel, icon: "🛢️" },
        { name: "Fuel Oil", price: data.result[0].fuelOil, icon: "🔥" }
      ];
    } catch (err) {
      console.error("Vue Fuel API Hatası:", err);
    }
  },

  methods: {
    logout() {
      localStorage.removeItem("userId");
      localStorage.removeItem("userEmail");
      localStorage.removeItem("userFirstName");
      localStorage.removeItem("userLastName");
      localStorage.removeItem("userRole");

      this.$router.push("/login");
    }
  }
};
</script>
