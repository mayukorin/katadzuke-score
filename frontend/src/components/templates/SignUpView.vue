<template>
  <div id="user-create-view">
    <v-container class="my-5">
      <v-row justify="center">
        <v-col cols="12" md="8">
          <SignUpCard />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import SignUpCard from "@/components/organisms/SignUpCard";
export default {
  name: "SignUpView",
  components: {
    SignUpCard,
  },
};
</script>
