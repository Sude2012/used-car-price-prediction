<template>
  <div class="min-h-screen relative overflow-hidden flex items-center justify-center px-4">
    <!-- Gradient background -->
    <div class="absolute inset-0 bg-gradient-to-br from-slate-950 via-indigo-950 to-fuchsia-950"></div>

    <!-- Soft blobs -->
    <div class="absolute -top-24 -left-24 h-72 w-72 rounded-full bg-fuchsia-500/25 blur-3xl"></div>
    <div class="absolute top-1/3 -right-24 h-80 w-80 rounded-full bg-indigo-500/25 blur-3xl"></div>
    <div class="absolute bottom-0 left-1/3 h-72 w-72 rounded-full bg-cyan-400/15 blur-3xl"></div>

    <!-- Card -->
    <div class="relative w-full max-w-md">
      <div class="rounded-3xl border border-white/10 bg-white/10 shadow-2xl backdrop-blur-xl">
        <div class="p-8 sm:p-9">
          <!-- Header -->
          <div class="flex items-center justify-between mb-7">
            <div>
              <h2 class="text-2xl font-bold text-white tracking-tight">Kayıt Ol ✨</h2>
              <p class="text-sm text-white/70 mt-1">
                Hesabını oluştur, tahminlere hemen başla
              </p>
            </div>

            <div
              class="h-11 w-11 rounded-2xl bg-white/10 border border-white/10 flex items-center justify-center"
            >
              <span class="text-lg">📝</span>
            </div>
          </div>

          <!-- Success -->
          <div
            v-if="success"
            class="mb-5 rounded-2xl border border-emerald-400/30 bg-emerald-500/10 px-4 py-3 text-emerald-100"
          >
            <p class="text-sm">
              Kayıt başarılı! Giriş sayfasına yönlendiriliyorsun...
            </p>
          </div>

          <!-- Error -->
          <div
            v-if="error"
            class="mb-5 rounded-2xl border border-rose-400/30 bg-rose-500/10 px-4 py-3 text-rose-100"
          >
            <p class="text-sm">{{ error }}</p>
          </div>

          <form @submit.prevent="register" class="space-y-4">
            <!-- First Name -->
            <div>
              <label class="block text-sm text-white/80 mb-2">Ad</label>
              <div class="relative">
                <span class="absolute left-3 top-1/2 -translate-y-1/2 text-white/50">👤</span>
                <input
                  v-model="firstName"
                  type="text"
                  autocomplete="given-name"
                  placeholder=""
                  class="w-full rounded-2xl bg-white/10 border border-white/10 px-10 py-3 text-white placeholder:text-white/40 outline-none focus:ring-2 focus:ring-fuchsia-400/40 focus:border-fuchsia-400/30 transition"
                  required
                />
              </div>
            </div>

            <!-- Last Name -->
            <div>
              <label class="block text-sm text-white/80 mb-2">Soyad</label>
              <div class="relative">
                <span class="absolute left-3 top-1/2 -translate-y-1/2 text-white/50">👤</span>
                <input
                  v-model="lastName"
                  type="text"
                  autocomplete="family-name"
                  placeholder=""
                  class="w-full rounded-2xl bg-white/10 border border-white/10 px-10 py-3 text-white placeholder:text-white/40 outline-none focus:ring-2 focus:ring-fuchsia-400/40 focus:border-fuchsia-400/30 transition"
                  required
                />
              </div>
            </div>

            <!-- Email -->
            <div>
              <label class="block text-sm text-white/80 mb-2">E-posta</label>
              <div class="relative">
                <span class="absolute left-3 top-1/2 -translate-y-1/2 text-white/50">✉️</span>
                <input
                  v-model="email"
                  type="email"
                  autocomplete="email"
                  placeholder="ornek@mail.com"
                  class="w-full rounded-2xl bg-white/10 border border-white/10 px-10 py-3 text-white placeholder:text-white/40 outline-none focus:ring-2 focus:ring-fuchsia-400/40 focus:border-fuchsia-400/30 transition"
                  required
                />
              </div>
            </div>

            <!-- Password -->
            <div>
              <label class="block text-sm text-white/80 mb-2">Şifre</label>
              <div class="relative">
                <span class="absolute left-3 top-1/2 -translate-y-1/2 text-white/50">🔒</span>

                <input
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="new-password"
                  placeholder="En az 6 karakter"
                  class="w-full rounded-2xl bg-white/10 border border-white/10 px-10 py-3 pr-12 text-white placeholder:text-white/40 outline-none focus:ring-2 focus:ring-fuchsia-400/40 focus:border-fuchsia-400/30 transition"
                  required
                />

                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-white/60 hover:text-white transition"
                  :aria-label="showPassword ? 'Şifreyi gizle' : 'Şifreyi göster'"
                >
                  {{ showPassword ? "🙈" : "👁️" }}
                </button>
              </div>

              <p class="mt-2 text-xs text-white/45">
                İpucu: Büyük/küçük harf + sayı kullanırsan daha güçlü olur.
              </p>
            </div>

            <!-- Submit -->
            <button
              type="submit"
              :disabled="loading"
              class="mt-2 w-full rounded-2xl bg-gradient-to-r from-emerald-500 to-cyan-500 py-3 font-semibold text-white shadow-lg shadow-emerald-500/20 hover:brightness-110 active:brightness-95 transition disabled:opacity-60 disabled:cursor-not-allowed"
            >
              <span v-if="!loading">Kayıt Ol</span>
              <span v-else class="inline-flex items-center gap-2">
                <span class="h-4 w-4 rounded-full border-2 border-white/50 border-t-white animate-spin"></span>
                Kayıt yapılıyor...
              </span>
            </button>
          </form>

          <!-- Footer -->
          <div class="mt-6 text-center text-sm text-white/70">
            Zaten hesabın var mı?
            <router-link
              to="/login"
              class="text-white font-semibold hover:underline underline-offset-4"
            >
              Giriş Yap
            </router-link>
          </div>

          <div class="mt-6 flex items-center gap-3">
            <div class="h-px flex-1 bg-white/10"></div>
            <span class="text-xs text-white/40">Hızlı ve güvenli</span>
            <div class="h-px flex-1 bg-white/10"></div>
          </div>

          <p class="mt-3 text-xs text-white/45 leading-relaxed">
            Kayıt olarak kullanım koşullarını kabul etmiş olursun. Verilerin güvenli şekilde işlenir.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { registerUser } from "../services/authService";

export default {
  name: "Register",
  data() {
    return {
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      success: false,
      error: null,
      showPassword: false,
      loading: false
    };
  },
  methods: {
    async register() {
      this.error = null;
      this.success = false;
      this.loading = true;

      try {
        const res = await registerUser({
          firstName: this.firstName,
          lastName: this.lastName,
          email: this.email,
          password: this.password
        });

        if (res && (res.status === 200 || res.status === 201)) {
          this.success = true;
          setTimeout(() => this.$router.push("/login"), 700);
        } else {
          this.error = "Kayıt başarısız (sunucudan beklenmeyen cevap).";
        }
      } catch (err) {
        console.error("REGISTER ERROR:", err);
        this.error = err?.response?.data?.message || "Kayıt başarısız!";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
