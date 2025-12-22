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
          <h1 class="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            🚗 Araç Fiyat Tahmini
          </h1>
          <p class="text-white/70 mt-1">
            Bilgileri doldur, yapay zeka destekli tahmini fiyatı gör.
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
          <!-- Alerts -->
          <div
            v-if="error"
            class="mb-5 rounded-2xl border border-rose-400/30 bg-rose-500/10 px-4 py-3 text-rose-100"
          >
            {{ error }}
          </div>

          <div
            v-if="savedMessage"
            class="mb-5 rounded-2xl border border-emerald-400/30 bg-emerald-500/10 px-4 py-3 text-emerald-100"
          >
            {{ savedMessage }}
          </div>

          <form @submit.prevent="predictPrice" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- MARKA -->
            <div>
              <label class="label">Marka</label>
              <div class="selectWrap">
                <select v-model="form.brandId" class="input selectInput" @change="onBrandChange">
                  <option :value="null">Seçiniz</option>
                  <option v-for="b in brands" :key="b.id" :value="b.id">
                    {{ b.name }}
                  </option>
                </select>
                <span class="selectArrow">▾</span>
              </div>
            </div>

            <!-- SERİ / MODEL -->
            <div>
              <label class="label">Seri / Model</label>
              <div class="selectWrap">
                <select v-model="form.modelId" class="input selectInput" :disabled="!form.brandId">
                  <option :value="null">Seçiniz</option>
                  <option v-for="m in models" :key="m.id" :value="m.id">
                    {{ m.name }}
                  </option>
                </select>
                <span class="selectArrow">▾</span>
              </div>
              <p v-if="!form.brandId" class="mt-2 text-xs text-white/45">
                Önce marka seçmelisin.
              </p>
            </div>

            <!-- YIL -->
            <div>
              <label class="label">Model Yılı</label>
              <input type="number" v-model.number="form.yil" class="input" placeholder="Örn: 2016" />
            </div>

            <!-- KM -->
            <div>
              <label class="label">Kilometre</label>
              <input type="number" v-model.number="form.km" class="input" placeholder="Örn: 125000" />
            </div>

            <!-- YAKIT -->
            <div>
              <label class="label">Yakıt</label>
              <div class="selectWrap">
                <select v-model="form.fuelTypeId" class="input selectInput">
                  <option :value="null">Seçiniz</option>
                  <option v-for="y in fuelTypes" :key="y.id" :value="y.id">
                    {{ y.name }}
                  </option>
                </select>
                <span class="selectArrow">▾</span>
              </div>
            </div>

            <!-- VİTES -->
            <div>
              <label class="label">Vites</label>
              <div class="selectWrap">
                <select v-model="form.gearTypeId" class="input selectInput">
                  <option :value="null">Seçiniz</option>
                  <option v-for="v in gearTypes" :key="v.id" :value="v.id">
                    {{ v.name }}
                  </option>
                </select>
                <span class="selectArrow">▾</span>
              </div>
            </div>

            <!-- RENK -->
            <div>
              <label class="label">Renk</label>
              <div class="selectWrap">
                <select v-model="form.colorId" class="input selectInput">
                  <option :value="null">Seçiniz</option>
                  <option v-for="r in colors" :key="r.id" :value="r.id">
                    {{ r.name }}
                  </option>
                </select>
                <span class="selectArrow">▾</span>
              </div>
            </div>

            <!-- KASA -->
            <div>
              <label class="label">Kasa Tipi</label>
              <div class="selectWrap">
                <select v-model="form.bodyTypeId" class="input selectInput">
                  <option :value="null">Seçiniz</option>
                  <option v-for="k in bodyTypes" :key="k.id" :value="k.id">
                    {{ k.name }}
                  </option>
                </select>
                <span class="selectArrow">▾</span>
              </div>
            </div>

            <!-- MOTOR -->
            <div>
              <label class="label">Motor Hacmi (cc)</label>
              <input type="number" v-model.number="form.motor_hacmi" class="input" placeholder="Örn: 1598" />
            </div>

            <div>
              <label class="label">Motor Gücü (hp)</label>
              <input type="number" v-model.number="form.motor_gucu" class="input" placeholder="Örn: 120" />
            </div>

            <!-- HASAR -->
            <div>
              <label class="label">Boya (adet)</label>
              <input type="number" v-model.number="form.boya" class="input" min="0" />
            </div>

            <div>
              <label class="label">Değişen (adet)</label>
              <input type="number" v-model.number="form.degisen" class="input" min="0" />
            </div>

            <!-- Submit -->
            <button
              class="md:col-span-2 rounded-2xl bg-gradient-to-r from-fuchsia-500 to-indigo-500
                     py-4 font-semibold text-white shadow-lg shadow-fuchsia-500/20
                     hover:brightness-110 active:brightness-95 transition
                     disabled:opacity-60 disabled:cursor-not-allowed"
              :disabled="loading"
            >
              <span v-if="!loading" class="inline-flex items-center justify-center gap-2">
                💸 Fiyatı Hesapla
              </span>
              <span v-else class="inline-flex items-center justify-center gap-2">
                <span class="h-4 w-4 rounded-full border-2 border-white/50 border-t-white animate-spin"></span>
                Hesaplanıyor...
              </span>
            </button>
          </form>

          <!-- Result -->
          <div
            v-if="result !== null"
            class="mt-6 rounded-3xl border border-emerald-400/30 bg-emerald-500/10 p-6 text-center"
          >
            <p class="text-white/80 text-sm">Tahmini Değer</p>
            <p class="text-3xl font-bold text-white mt-1">
              {{ Number(result).toLocaleString("tr-TR") }} ₺
            </p>
            <p class="text-emerald-100/90 mt-2 text-sm" v-if="savedMessage">
              {{ savedMessage }}
            </p>
          </div>

          <div class="mt-6 flex items-center gap-3">
            <div class="h-px flex-1 bg-white/10"></div>
            <span class="text-xs text-white/40">İpucu</span>
            <div class="h-px flex-1 bg-white/10"></div>
          </div>

          <p class="mt-3 text-xs text-white/45 leading-relaxed">
            Marka/Model seçiminden sonra diğer bilgileri mümkün olduğunca doğru girmen tahmin kalitesini artırır.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  data() {
    return {
      loading: false,
      result: null,
      error: null,
      savedMessage: null,

      brands: [],
      models: [],
      fuelTypes: [],
      gearTypes: [],
      colors: [],
      bodyTypes: [],

      form: {
        brandId: null,
        modelId: null,
        fuelTypeId: null,
        gearTypeId: null,
        colorId: null,
        bodyTypeId: null,

        yil: null,
        km: null,
        motor_hacmi: null,
        motor_gucu: null,
        boya: 0,
        degisen: 0
      }
    };
  },

  async mounted() {
    await this.loadLookups();
  },

  methods: {
    async loadLookups() {
      try {
        const [brands, fuel, gear, colors, body] = await Promise.all([
          api.get("/Lookup/brands"),
          api.get("/Lookup/fueltypes"),
          api.get("/Lookup/geartypes"),
          api.get("/Lookup/colors"),
          api.get("/Lookup/bodytypes")
        ]);

        this.brands = brands.data;
        this.fuelTypes = fuel.data;
        this.gearTypes = gear.data;
        this.colors = colors.data;
        this.bodyTypes = body.data;

        this.form.fuelTypeId = this.fuelTypes[0]?.id ?? null;
        this.form.gearTypeId = this.gearTypes[0]?.id ?? null;
        this.form.colorId = this.colors[0]?.id ?? null;
        this.form.bodyTypeId = this.bodyTypes[0]?.id ?? null;
      } catch (e) {
        console.error(e);
        this.error = "Lookup verileri alınamadı. ApiGateway çalışıyor mu?";
      }
    },

    async onBrandChange() {
      this.form.modelId = null;
      this.models = [];

      if (!this.form.brandId) return;

      try {
        const res = await api.get(`/Lookup/models?brandId=${this.form.brandId}`);
        this.models = res.data;
      } catch (e) {
        console.error(e);
        this.error = "Model listesi alınamadı.";
      }
    },

    getNameById(list, id) {
      const x = list.find(i => i.id === id);
      return x ? x.name : "";
    },

    async predictPrice() {
      this.loading = true;
      this.error = null;
      this.savedMessage = null;
      this.result = null;

      try {
        const userId = Number(localStorage.getItem("userId"));
        if (!userId) {
          this.error = "Giriş yapılmamış. Lütfen tekrar giriş yap.";
          return;
        }

        if (!this.form.brandId || !this.form.modelId) {
          this.error = "Lütfen marka ve model seç.";
          return;
        }

        const pythonPayload = {
          marka: this.getNameById(this.brands, this.form.brandId),
          seri: this.getNameById(this.models, this.form.modelId),
          yil: this.form.yil,
          km: this.form.km,
          yakit: this.getNameById(this.fuelTypes, this.form.fuelTypeId),
          vites: this.getNameById(this.gearTypes, this.form.gearTypeId),
          renk: this.getNameById(this.colors, this.form.colorId),
          kasa: this.getNameById(this.bodyTypes, this.form.bodyTypeId),
          motor_hacmi: this.form.motor_hacmi,
          motor_gucu: this.form.motor_gucu,
          boya: this.form.boya,
          degisen: this.form.degisen
        };

        const res = await fetch("http://127.0.0.1:8000/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(pythonPayload)
        });

        if (!res.ok) throw new Error("Python API hata döndü.");
        const data = await res.json();
        this.result = data.predicted_price;

        const savePayload = {
          userId,
          carId: 2,
          predictedPrice: Number(this.result),
          modelName: `${pythonPayload.marka} ${pythonPayload.seri}`,

          inputYear: this.form.yil,
          inputKilometer: this.form.km,

          inputBrandId: this.form.brandId,
          inputModelId: this.form.modelId,
          inputFuelTypeId: this.form.fuelTypeId,
          inputGearTypeId: this.form.gearTypeId,
          inputColorId: this.form.colorId,
          inputBodyTypeId: this.form.bodyTypeId
        };

        await api.post("/Predictions/save", savePayload);
        this.savedMessage = "";
      } catch (e) {
        console.error(e);
        this.error = "Tahmin alınamadı veya veritabanına kaydedilemedi.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Glass form inputs */
.input {
  @apply w-full rounded-2xl bg-white/10 border border-white/10 px-4 py-3 text-white
  placeholder:text-white/40 outline-none transition
  focus:ring-2 focus:ring-fuchsia-400/40 focus:border-fuchsia-400/30;
}

.label {
  @apply block mb-2 text-sm text-white/80 font-medium;
}

/* Select wrapper */
.selectWrap {
  position: relative;
}

/* Select arrow */
.selectArrow {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: rgba(255, 255, 255, 0.55);
  font-size: 14px;
}

/* Hide native arrow & reserve space for custom arrow */
.selectInput {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  padding-right: 42px;
}

/* 🔥 Dropdown options (fix Windows/Chrome blue highlight look) */
.selectInput option,
.selectInput optgroup {
  background-color: #0b1220;
  color: #ffffff;
}

/* Disabled select look */
select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
