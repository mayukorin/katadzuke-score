<template>
  <v-card class="login-card px-3">
    <v-card-title>
      <span class="headline">KDS</span>
    </v-card-title>
    <v-card-text>
      <SignInForm @signin-button-click="handleSignin" :is-loading="isLoading" />
    </v-card-text>
  </v-card>
</template>

<script>
import SignInForm from "@/components/molecules/SignInForm";
export default {
  name: "SignInCard",
  components: {
    SignInForm,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  /*
  created() {
    this.$store.dispatch("flashMessage/clearMessages");
  },
  */
  methods: {
    handleSignin(authInfo) {
      this.isLoading = true;
      this.$store
        .dispatch("auth/signin", authInfo)
        .then(() => {
          return this.$store.dispatch("auth/getUserInfo");
        })
        .then(() => {
          let signInSuccessMessage = "ログインしました";
          this.$store.dispatch("flashMessage/setSuccessMessage", {
            messages: [signInSuccessMessage],
          });
          const next = this.$route.query.next || "/";
          this.$router.replace(next);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
};
</script>
