<template>
  <!-- Background -->
  <div class="min-h-screen relative overflow-hidden flex items-center justify-center px-4">
    <!-- Gradient background -->
    <div
      class="absolute inset-0 bg-gradient-to-br from-slate-950 via-indigo-950 to-fuchsia-950"
    ></div>

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
              <h2 class="text-2xl font-bold text-white tracking-tight">Hoş geldin 👋</h2>
              <p class="text-sm text-white/70 mt-1">
                2. El Araç Fiyat Tahmini için giriş yap
              </p>
            </div>

            
          </div>

          <!-- Error -->
          <div
            v-if="error"
            class="mb-5 rounded-2xl border border-rose-400/30 bg-rose-500/10 px-4 py-3 text-rose-100"
          >
            <p class="text-sm">{{ error }}</p>
          </div>

          <form @submit.prevent="login" class="space-y-4">
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
                  autocomplete="current-password"
                  placeholder="••••••••"
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
            </div>

            <!-- Row -->
            <div class="flex items-center justify-between pt-1">
              <label class="inline-flex items-center gap-2 text-sm text-white/70 select-none">
                <input
                  type="checkbox"
                  v-model="rememberMe"
                  class="h-4 w-4 rounded border-white/20 bg-white/10 text-fuchsia-400 focus:ring-fuchsia-400/30"
                />
                Beni hatırla
              </label>

              <button
                type="button"
                class="text-sm text-white/70 hover:text-white transition underline underline-offset-4"
                @click="fakeForgot()"
              >
                Şifremi unuttum
              </button>
            </div>

            <!-- Submit -->
            <button
              type="submit"
              :disabled="loading"
              class="mt-2 w-full rounded-2xl bg-gradient-to-r from-fuchsia-500 to-indigo-500 py-3 font-semibold text-white shadow-lg shadow-fuchsia-500/20 hover:brightness-110 active:brightness-95 transition disabled:opacity-60 disabled:cursor-not-allowed"
            >
              <span v-if="!loading">Giriş Yap</span>
              <span v-else class="inline-flex items-center gap-2">
                <span class="h-4 w-4 rounded-full border-2 border-white/50 border-t-white animate-spin"></span>
                Giriş yapılıyor...
              </span>
            </button>
          </form>

          <!-- Footer -->
          <div class="mt-6 text-center text-sm text-white/70">
            Hesabın yok mu?
            <router-link
              to="/register"
              class="text-white font-semibold hover:underline underline-offset-4"
            >
              Kayıt Ol
            </router-link>
          </div>

          <div class="mt-6 flex items-center gap-3">
            <div class="h-px flex-1 bg-white/10"></div>
            <span class="text-xs text-white/40">Güvenli giriş</span>
            <div class="h-px flex-1 bg-white/10"></div>
          </div>

          <p class="mt-3 text-xs text-white/45 leading-relaxed">
            Giriş yaptığında kullanıcı bilgilerin cihazında saklanır. Ortak bilgisayar kullanıyorsan
            çıkış yapmayı unutma.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { loginUser } from "../services/authService";

export default {
  name: "Login",
  data() {
    return {
      email: "",
      password: "",
      error: null,
      showPassword: false,
      rememberMe: true,
      loading: false
    };
  },
  methods: {
    async login() {
      this.error = null;
      this.loading = true;

      try {
        const res = await loginUser({
          email: this.email,
          password: this.password
        });

        console.log("LOGIN RESPONSE:", res.data);
        console.log("USER OBJ:", res.data.user);

        const user = res.data.user;

        // ✅ localStorage'a kaydet (senin mevcut yapın)
        localStorage.setItem("userId", user.userId);
        localStorage.setItem("userEmail", user.email);
        localStorage.setItem("userFirstName", user.firstName);
        localStorage.setItem("userLastName", user.lastName);
        localStorage.setItem("userRole", user.role);

        // İstersen "Beni hatırla" false ise burada temizleyebilirsin:
        // if (!this.rememberMe) { ...sessionStorage kullanımı vs. }

        this.$router.push("/dashboard");
      } catch (err) {
        this.error = "E-posta veya şifre hatalı!";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    fakeForgot() {
      // İstersen /forgot-password sayfasına yönlendirebiliriz
      alert("Şifre sıfırlama sayfasını eklersen buraya yönlendiririz 🙂");
    }
  }
};
</script>
