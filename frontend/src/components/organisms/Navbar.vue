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
      <span v-if="rewardThisMonth >= 0 && isSignIn" class="white--text">
        今月のご褒美：
        <br />
        <span class="accent--text">
          {{ rewardThisMonth }}
        </span>
        円
      </span>
      <span v-else-if="rewardThisMonth < 0 && isSignIn" class="white--text">
        今月の罰金：
        <br />
        <span class="accent--text">
          {{ -1 * rewardThisMonth }}
        </span>
        円
      </span>
      <v-btn v-if="isSignIn" text color="white" @click="signout">
        <span>ログアウト</span>
        <v-icon right>mdi-exit-to-app</v-icon>
      </v-btn>
      <v-btn v-else text color="white" @click="signin">
        <span>ログイン</span>
        <v-icon right>mdi-exit-to-app</v-icon>
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
    rewardThisMonth() {
      return this.$store.state.auth.rewardThisMonth;
    },
  },
  methods: {
    setSnacFalse: function () {
      this.snac = false;
    },
    setSnacTrue: function () {
      this.snac = true;
    },
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
    handleDrawer() {
      this.$emit("handle-drawer");
    },
  },
};
</script>
