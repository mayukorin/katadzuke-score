<template>
  <div id="login-view">
    <v-container class="my-5">
      <v-row justify="center">
        <v-col cols="11" md="8">
          <SignInCard />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import SignInCard from "@/components/organisms/SignInCard";
export default {
  name: "SignInView",
  components: {
    SignInCard,
  },
};
</script>
