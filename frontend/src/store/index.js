import Vue from "vue";
import Vuex from "vuex";
import api from "@/services/api";

Vue.use(Vuex);

const authModule = {
  namespaced: true,
  state: {
    email: "",
    username: "",
    isSignIn: false,
    // TODO: 動的に変化
    threshouldRewardScore: 60,
    threshouldFineScore: 20,
    AmountOfReward: 100,
    AmountOfFine: 200,
    rewardThisMonth: 0,
  },
  mutations: {
    set(state, payload) {
      state.email = payload.user.email;
      state.username = payload.user.username;
      state.isSignIn = true;
    },
    setRewardThisMonth(state, payload) {
      state.rewardThisMonth = payload.amount_of_money;
    },
    clear(state) {
      (state.email = ""), (state.username = "");
      state.isSignIn = false;
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
          context.dispatch("renew");
          return context.dispatch("getRewardThisMonth");
        });
    },
    signup(context, payload) {
      console.log(payload);
      // ここでapiでDjangoと接続
      return api({
        method: "post",
        url: "/signup/",
        data: payload,
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
    signout(context) {
      localStorage.removeItem("access");
      context.commit("clear");
    },
    getRewardThisMonth(context) {
      return api.get("/reward-this-month/").then((response) => {
        console.log(response.data);
        context.commit("setRewardThisMonth", response.data);
        return response.data;
      });
    },
  },
};

const roomPhotoModule = {
  namespaced: true,
  state: {
    roomPhotos: [],
  },
  mutations: {
    set(state, payload) {
      state.roomPhotos = payload.roomPhotos;
    },
    setRoomPhoto(state, payload) {
      console.log("setRoomPhoto");
      console.log(payload);
      let roomPhoto = state.roomPhotos.find(
        (roomPhoto) => roomPhoto.pk == payload.pk
      );
      roomPhoto.photo_url = payload.photo_url;
      roomPhoto.percent_of_floors = payload.percent_of_floors;
    },
    clear(state) {
      state.roomPhotos = [];
    },
  },
  actions: {
    upload(context, payload) {
      console.log(payload);
      console.log(process.env.VUE_APP_ROOT_API);
      return api({
        method: "post",
        url: "/room-photos/" + payload.roomPhotoPk + "/room-photo-upload/",
        data: {
          roomPhotoBase64Content: payload.roomPhotoBase64Content,
        },
      }).then((response) => {
        context.commit("setRoomPhoto", response.data);
        return response.data;
      });
    },
    list(context) {
      return api({
        method: "get",
        url: "/room-photos/",
      }).then((response) => {
        console.log(response);
        context.commit("set", { roomPhotos: response.data });
      });
    },
  },
};

const flashMessageModule = {
  namespaced: true,
  state: {
    messages: [],
    color: "",
  },
  mutations: {
    set(state, payload) {
      if (payload.error) {
        state.messages = payload.error;
        state.color = "error";
      } else if (payload.warning) {
        state.messages = payload.warning;
        state.color = "accent";
      } else if (payload.success) {
        state.messages = payload.success;
        state.color = "primaryDark";
      }
    },
    clear(state) {
      state.messages = [];
      state.color = "";
    },
  },
  actions: {
    setErrorMessage(context, payload) {
      context.commit("clear");
      console.log("actions");
      console.log(payload.message);
      context.commit("set", { error: payload.messages });
    },
    setWarningMessages(context, payload) {
      context.commit("clear");
      context.commit("set", { warning: payload.messages });
    },
    setSuccessMessage(context, payload) {
      context.commit("clear");
      context.commit("set", { success: payload.messages });
    },
    clearMessages(context) {
      context.commit("clear");
    },
  },
};

const store = new Vuex.Store({
  modules: {
    roomPhotos: roomPhotoModule,
    auth: authModule,
    flashMessage: flashMessageModule,
  },
});

export default store;
