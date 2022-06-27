import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "@/components/templates/HomeView";
import SignUp from "@/components/templates/SignUpView";
import SignIn from "@/components/templates/SignInView";
import FullScoreRoomPhotoUpload from "@/components/templates/FullScoreRoomPhotoUploadView";
import RewardAndFineUpdate from "@/components/templates/RewardAndFineUpdateView";
import store from "@/store";
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
  {
    path: "/full-score-room-photo-upload",
    name: "fullScoreRoomPhotoUpload",
    component: FullScoreRoomPhotoUpload,
    meta: { requiresAuth: true },
  },
  {
    path: "/fine-and-reward-update",
    name: "RewardAndFineUpdate",
    component: RewardAndFineUpdate,
    meta: { requiresAuth: true },
  },
];

const router = new VueRouter({
  mode: "history",
  routes,
});

router.beforeEach((to, from, next) => {
  const isSignIn = store.state.auth.isSignIn;
  const token = localStorage.getItem("access");
  console.log("to.path=", to.path);
  console.log("isSignIn=", isSignIn);

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!isSignIn) {
      console.log("User is not logged in.");
      if (token != null) {
        console.log("Try to renew user info.");
        store
          .dispatch("auth/renew")
          .then(() => {
            console.log("Succeeded to renew. So, free to next.");
            next();
          })
          .catch(() => {
            forceToSignInPage(to);
          });
      } else {
        forceToSignInPage(to);
      }
    } else {
      console.log("User is already logged in. So, free to next.");
      next();
    }
  } else {
    console.log("Go to public page.");
    next();
  }
});

function forceToSignInPage(to) {
  console.log("Force to login page.");
  router.replace({
    path: "/sign-in",
    query: { next: to.fullPath },
  });
}

export default router;
