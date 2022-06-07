import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import SignUp from "@/components/templates/SignUpView";
import SignIn from "@/components/templates/SignInView";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: "/sign-up",
    name: "signUp",
    component: SignUp,
  },
  {
    path: "/sign-in",
    name: "signIn",
    component: SignIn,
  },
];

const router = new VueRouter({
  mode: "history",
  // base: process.env.BASE_URL,
  routes,
});

export default router;
