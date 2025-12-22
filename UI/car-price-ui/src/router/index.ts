import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Dashboard from "../views/Dashboard.vue";
import CarPredict from "../views/CarPredict.vue";
import History from "../views/History.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/login" },
    { path: "/login", component: Login },
    { path: "/register", component: Register },
    { path: "/dashboard", component: Dashboard },
    { path: "/predict", component: CarPredict },
    { path: "/history", component: History }, // 👈 EKLENEN
  ],
});

export default router;
