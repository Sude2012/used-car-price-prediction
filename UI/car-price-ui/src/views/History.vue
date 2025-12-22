<template>
  <div class="min-h-screen relative overflow-hidden px-4 py-10">
    <!-- Gradient background -->
    <div class="absolute inset-0 bg-gradient-to-br from-slate-950 via-indigo-950 to-fuchsia-950"></div>

    <!-- Soft blobs -->
    <div class="absolute -top-24 -left-24 h-72 w-72 rounded-full bg-fuchsia-500/25 blur-3xl"></div>
    <div class="absolute top-1/3 -right-24 h-80 w-80 rounded-full bg-indigo-500/25 blur-3xl"></div>
    <div class="absolute bottom-0 left-1/3 h-72 w-72 rounded-full bg-cyan-400/15 blur-3xl"></div>

    <div class="relative max-w-5xl mx-auto">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h2 class="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            📌 Geçmiş Tahminlerim
          </h2>
          <p class="text-white/70 mt-1">
            Daha önce yaptığın tahminleri buradan görüntüleyebilirsin.
          </p>
        </div>

        <router-link
          to="/dashboard"
          class="inline-flex items-center justify-center gap-2 rounded-2xl
                 bg-white/10 border border-white/10 px-5 py-3
                 text-white font-semibold hover:bg-white/15 transition"
        >
          ← Dashboard
        </router-link>
      </div>

      <!-- Main glass card -->
      <div class="rounded-3xl border border-white/10 bg-white/10 shadow-2xl backdrop-blur-xl">
        <div class="p-6 sm:p-8">
          <!-- Loading -->
          <div
            v-if="loading"
            class="flex items-center gap-3 text-white/80"
          >
            <span class="h-4 w-4 rounded-full border-2 border-white/40 border-t-white animate-spin"></span>
            Yükleniyor...
          </div>

          <!-- Error -->
          <div
            v-else-if="error"
            class="rounded-2xl border border-rose-400/30 bg-rose-500/10 px-4 py-3 text-rose-100"
          >
            {{ error }}
          </div>

          <!-- Empty -->
          <div
            v-else-if="items.length === 0"
            class="rounded-2xl border border-white/10 bg-white/5 px-5 py-6 text-center"
          >
            <div class="text-3xl mb-2">🗂️</div>
            <p class="text-white/80 font-semibold">Henüz kayıtlı tahminin yok.</p>
            <p class="text-white/55 text-sm mt-1">
              İlk tahminini yapmak için “Yeni Tahmin” sayfasına gidebilirsin.
            </p>

            <router-link
              to="/predict"
              class="mt-4 inline-flex items-center justify-center gap-2 rounded-2xl
                     bg-gradient-to-r from-fuchsia-500 to-indigo-500
                     px-6 py-3 text-white font-semibold
                     shadow-lg shadow-fuchsia-500/20
                     hover:brightness-110 active:brightness-95 transition"
            >
              🚘 Yeni Tahmin Yap
            </router-link>
          </div>

          <!-- Table -->
          <div v-else class="overflow-x-auto rounded-2xl border border-white/10">
            <table class="w-full text-sm">
              <thead class="bg-white/5">
                <tr class="text-white/80">
                  <th class="p-4 text-left font-semibold">Tarih</th>
                  <th class="p-4 text-left font-semibold">Model</th>
                  <th class="p-4 text-left font-semibold">Yıl</th>
                  <th class="p-4 text-left font-semibold">KM</th>
                  <th class="p-4 text-left font-semibold">Tahmin (₺)</th>
                </tr>
              </thead>

              <tbody>
                <tr
                  v-for="p in items"
                  :key="p.predictionId"
                  class="border-t border-white/10 hover:bg-white/5 transition"
                >
                  <td class="p-4 text-white/80 whitespace-nowrap">
                    {{ formatDate(p.createdAt || p.predictionDate) }}
                  </td>
                  <td class="p-4 text-white/80">
                    {{ p.modelName || "-" }}
                  </td>
                  <td class="p-4 text-white/80">
                    {{ p.inputYear ?? "-" }}
                  </td>
                  <td class="p-4 text-white/80">
                    {{ p.inputKilometer ?? "-" }}
                  </td>
                  <td class="p-4 font-semibold text-white whitespace-nowrap">
                    {{ formatMoney(p.predictedPrice) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Small footer note -->
          <p v-if="!loading && !error && items.length > 0" class="text-xs text-white/45 mt-4">
            Not: Tarihler cihaz saatine göre gösterilir. (tr-TR)
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getMyPredictions } from "../services/predictionService";

export default {
  name: "History",
  data() {
    return {
      loading: true,
      error: null,
      items: [],
    };
  },
  async mounted() {
    try {
      const userId = localStorage.getItem("userId");
      if (!userId) {
        this.error = "Giriş yapılmamış. Lütfen tekrar giriş yap.";
        return;
      }

      const res = await getMyPredictions(userId);
      this.items = Array.isArray(res.data) ? res.data : [];
    } catch (e) {
      console.error(e);
      this.error = "Geçmiş tahminler alınamadı.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatDate(d) {
      if (!d) return "-";
      return new Date(d).toLocaleString("tr-TR");
    },
    formatMoney(v) {
      if (v === null || v === undefined) return "-";
      return Number(v).toLocaleString("tr-TR") + " ₺";
    },
  },
};
</script>
