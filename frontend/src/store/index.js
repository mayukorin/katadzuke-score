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
    threshouldRewardScore: 0,
    threshouldFineScore: 0,
    amountOfReward: 0,
    amountOfFine: 0,
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
    setUserInfo(state, payload) {
      state.threshouldRewardScore = payload.threshould_reward_score;
      state.threshouldFineScore = payload.threshould_fine_score;
      state.amountOfReward = payload.amount_of_reward;
      state.amountOfFine = payload.amount_of_fine;
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
          context.dispatch("getRewardThisMonth");
          return context.dispatch("getUserInfo");
        });
    },
    signup(context, payload) {
      console.log(payload);
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
    updateUserInfo(context, payload) {
      console.log(payload);
      return api({
        method: "patch",
        url: "/user-info-update/",
        data: payload,
      }).then((response) => {
        return context.commit("setUserInfo", response.data);
      });
    },
    getUserInfo(context) {
      return api("/user-info/").then((response) => {
        console.log(response.data);
        context.commit("setUserInfo", response.data);
        return context.dispatch(
          "roomPhotos/setFullScoreRoomPhotoURL",
          response.data,
          { root: true }
        );
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
    setFullScoreRoomPhotoURL(state, payload) {
      state.fullScoreRoomPhotoURL = payload.full_score_photo_url;
      console.log(state.fullScoreRoomPhotoURL);
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
    uploadFullScoreRoomPhoto(context, payload) {
      return api({
        method: "post",
        url: "/room-photos/full-score/",
        data: {
          roomPhotoBase64Content: payload.roomPhotoBase64Content,
        },
      }).then((response) => {
        console.log(response);
        context.commit("setFullScoreRoomPhotoURL", response.data);
      });
    },
    setFullScoreRoomPhotoURL(context, payload) {
      return context.commit("setFullScoreRoomPhotoURL", payload);
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
