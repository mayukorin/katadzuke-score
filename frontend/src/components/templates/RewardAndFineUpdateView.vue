<template>
  <div id="login-view">
    <v-container class="my-5">
      <v-row justify="center">
        <v-col cols="11" md="8">
          <RewardAndFineUpdateCard />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import RewardAndFineUpdateCard from "@/components/organisms/RewardAndFineUpdateCard";
export default {
  name: "RewardAndFineUpdateView",
  components: {
    RewardAndFineUpdateCard,
  },
};
</script>
