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
  },
  mutations: {
    setRewardThisMonth(state, payload) {
      state.rewardThisMonth = payload.amount_of_money;
    },
    clear(state) {
      (state.email = ""), (state.username = "");
      state.isSignIn = false;
    },
    setAll(state, payload) {
      console.log("setAll");
      state.email = payload.email;
      state.username = payload.username;
      state.isSignIn = true;
    },
  },
  actions: {
    signin(context, payload) {
      console.log("signin");
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
      return api({
        method: "post",
        url: "/signup/",
        data: payload,
      }).then((response) => {
        return response;
      });
    },
    renew() {
      console.log("renew");
      return api.get("/auth/users/me");
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
    updateUserInfo(context, payload) {
      console.log(payload);
      return api({
        method: "patch",
        url: "/user-info-update/",
        data: payload,
      }).then((response) => {
        return context.commit("setAll", response.data);
      });
    },
    getUserInfo(context) {
      return api("/user-info/").then((response) => {
        console.log("get user info");
        context.commit("setAll", response.data);
        context.commit("reward/setAll", response.data, { root: true });
      });
    },
  },
};

const roomPhotoModule = {
  namespaced: true,
  state: {
    roomPhotos: [],
    fullScoreRoomPhotoURL: "",
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
      roomPhoto.katadzuke_score = payload.katadzuke_score;
    },
    setFullScoreRoomPhotoURL(state, full_score_photo_url) {
      state.fullScoreRoomPhotoURL = full_score_photo_url;
      console.log(state.fullScoreRoomPhotoURL);
    },
    clear(state) {
      state.roomPhotos = [];
      state.fullScoreRoomPhotoURL = "";
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
    uploadFullScoreRoomPhoto(context, payload) {
      return api({
        method: "post",
        url: "/room-photos/full-score/",
        data: {
          roomPhotoBase64Content: payload.roomPhotoBase64Content,
        },
      }).then((response) => {
        console.log(response);
        context.commit("setFullScoreRoomPhotoURL", response.data.photo_url);
      });
    },
    setFullScoreRoomPhotoURL(context, payload) {
      return context.commit(
        "setFullScoreRoomPhotoURL",
        payload.full_score_photo.photo_url
      );
    },
    clear(context) {
      return context.commit("clear");
    },
  },
};

const rewardModule = {
  namespaced: true,
  state: {
    threshouldRewardScore: 0,
    threshouldFineScore: 0,
    amountOfReward: 0,
    amountOfFine: 0,
    amountOfRewardThisMonth: 0,
  },
  mutations: {
    setAll(state, payload) {
      console.log("setAll");
      console.log(payload);
      state.threshouldRewardScore = payload.threshould_reward_score;
      state.threshouldFineScore = payload.threshould_fine_score;
      state.amountOfReward = payload.amount_of_reward;
      state.amountOfFine = payload.amount_of_fine;
      state.amountOfRewardThisMonth = payload.amount_of_reward_this_month;
    },
    setAmountOfRewardThisMonth(state, payload) {
      state.amountOfRewardThisMonth = payload.amount_of_reward_this_month;
    },
  },
  actions: {
    updateAmountOfRewardThisMonth(context, payload) {
      return api({
        method: "post",
        url: "/reward-this-month-update/",
        data: {
          prev_room_photo_score: payload.prevRoomPhotoScore,
          new_room_photo_score: payload.newRoomPhotoScore,
        },
      }).then((response) => {
        console.log(response);
        context.commit("setAmountOfRewardThisMonth", {
          amount_of_reward_this_month: response.data.amount_of_money,
        });
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
      console.log("success!");
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
    reward: rewardModule,
    flashMessage: flashMessageModule,
  },
});

export default store;
