import Vue from "vue";
import Vuex from "vuex";
import api from "@/services/api";

Vue.use(Vuex);

const authModule = {
  namespaced: true,
  state: {
    email: "",
    username: "",
    isLoggedIn: false,
  },
  mutations: {
    set(state, payload) {
      state.email = payload.user.email;
      state.username = payload.user.username;
      state.isLoggedIn = true;
    },
    clear(state) {
      (state.email = ""), (state.username = "");
      state.isLoggedIn = false;
    },
  },
  actions: {
    signin(context, payload) {
      return api
        .post("/auth/jwt/create/", {
          email: payload.email,
          password: payload.password,
        })
        .then((response) => {
          localStorage.setItem("access", response.data.access);
          return context.dispatch("renew");
        });
    },
    signup(context, payload) {
      console.log(payload);
      // ここでapiでDjangoと接続
      return api({
        method: "post",
        url: "/signup/",
        data: {
          email: payload.email,
          password: payload.password,
          username: payload.username,
        },
      }).then((response) => {
        // 作成したアカウントを使ってログイン処理もする
        return context.dispatch("signin", {
          email: response.data.email,
          password: payload.password,
        });
      });
    },
    renew(context) {
      return api.get("/auth/users/me").then((response) => {
        const user = response.data;
        context.commit("set", { user: user });
      });
    },
    logout(context) {
      // token をリフレッシュするため，1 回削除
      localStorage.removeItem("access");
      context.commit("clear");
    },
  },
};

const roomPhotoModule = {
  namespaced: true,
  actions: {
    upload(context, payload) {
      console.log(payload);
      console.log(process.env.VUE_APP_ROOT_API);
      return api({
        method: "post",
        url: "/room-photo-upload/",
        data: payload,
      }).then((response) => {
        console.log(response);
      });
    },
  },
};

const store = new Vuex.Store({
  modules: {
    roomPhotos: roomPhotoModule,
    auth: authModule,
  },
});

export default store;
