<template>
  <nav>
    <v-snackbar v-model="snac" top :color="flashMessage.color">
      <div v-for="message in flashMessage.messages" :key="message">
        {{ message }}
      </div>
    </v-snackbar>
    <v-app-bar app color="primary">
      <v-toolbar-title class="text-uppercase white--text">
        <span class="font-weight-light">KDS</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <span v-if="amountOfRewardThisMonth >= 0 && isSignIn" class="white--text">
        今月のご褒美：
        <span class="accent--text">
          {{ amountOfRewardThisMonth }}
        </span>
        円
      </span>
      <span
        v-else-if="amountOfRewardThisMonth < 0 && isSignIn"
        class="white--text"
      >
        今月の罰金：
        <br />
        <span class="accent--text">
          {{ -1 * amountOfRewardThisMonth }}
        </span>
        円
      </span>
      <v-menu offset-y v-if="isSignIn">
        <template v-slot:activator="{ on, attrs }">
          <v-btn text v-bind="attrs" v-on="on" color="white">
            <v-icon left>mdi-chevron-down</v-icon>
            <span class="white--text">Menu</span>
          </v-btn>
        </template>
        <v-list>
          <v-list-item router to="/">
            <v-list-item-content>
              <v-list-item-title>トップページ</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item router to="/full-score-room-photo-upload">
            <v-list-item-content>
              <v-list-item-title>100点満点の部屋登録</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item router to="/fine-and-reward-update">
            <v-list-item-content>
              <v-list-item-title>ご褒美と罰金の設定</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="signout">
            <v-list-item-content>
              <v-list-item-title>ログアウト</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn v-if="!isSignIn" text color="white" @click="signin">
        <span>ログイン</span>
        <v-icon right>mdi-exit-to-app</v-icon>
      </v-btn>
      <v-btn v-if="!isSignIn" text color="white" @click="signup">
        <span>新規登録</span>
      </v-btn>
    </v-app-bar>
  </nav>
</template>
<script>
// import Appbar from "@/components/organisms/Appbar";

export default {
  name: "NavBar",
  data() {
    return {
      drawer: false,
      snac: true,
    };
  },
  computed: {
    isSignIn() {
      return this.$store.state.auth.isSignIn;
    },
    flashMessage() {
      let messages = this.$store.state.flashMessage.messages;
      console.log(messages);
      if (messages.length > 0) {
        this.setSnacTrue();
        if (
          messages.indexOf("ログインの有効期限切れです．") != -1 &&
          this.$route.path != "/sign-in"
        ) {
          console.log("ok");
          this.$router.replace({
            path: "/sign-in",
            query: { next: this.$route.path },
          });
        }
      } else this.setSnacFalse();
      return this.$store.state.flashMessage;
    },
    amountOfRewardThisMonth() {
      return this.$store.state.reward.amountOfRewardThisMonth;
    },
  },
  methods: {
    setSnacFalse: function () {
      this.snac = false;
    },
    setSnacTrue: function () {
      this.snac = true;
    },
    // 後でまとめる
    signout() {
      this.$store.dispatch("auth/signout");
      this.$store.dispatch("flashMessage/setSuccessMessage", {
        messages: ["ログアウトしました"],
      });
      this.$router.replace("/sign-in");
    },
    signin() {
      this.$router.replace("/sign-in");
    },
    signup() {
      this.$router.replace("/sign-up");
    },
    handleDrawer() {
      this.$emit("handle-drawer");
    },
  },
};
</script>
