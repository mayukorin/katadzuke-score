<template>
  <v-card class="login-card px-3">
    <v-card-title>
      <span class="headline">e-resolve</span>
    </v-card-title>
    <v-card-text>
      <SignUpForm @signup-button-click="handleSignUp" :is-loading="isLoading" />
    </v-card-text>
  </v-card>
</template>

<script>
import SignUpForm from "@/components/molecules/SignUpForm";
export default {
  name: "SignUpCard",
  components: {
    SignUpForm,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  methods: {
    handleSignUp(userInfo) {
      this.isLoading = true;
      return this.$store
        .dispatch("auth/signup", userInfo)
        .then(() => {
          console.log("signin and login succeeded.");
          const next = "/";
          this.$router.replace(next);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
};
</script>
