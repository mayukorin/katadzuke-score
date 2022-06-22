<template>
  <v-card class="login-card px-3">
    <v-card-title>
      <span class="headline">ご褒美と罰金の設定</span>
    </v-card-title>
    <v-card-text>
      <RewardAndFineUpdateForm
        :is-loading="isLoading"
        :threshould-reward-score="threshouldRewardScore"
        :threshould-fine-score="threshouldFineScore"
        :amount-of-reward="amountOfReward"
        :amount-of-fine="amountOfFine"
        @update-button-click="handleUpdate"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import RewardAndFineUpdateForm from "@/components/molecules/RewardAndFineUpdateForm";
export default {
  name: "RewardAndFineUpdateCard",
  components: {
    RewardAndFineUpdateForm,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  methods: {
    handleUpdate(rewardAndFineInfo) {
      this.isLoading = true;
      return this.$store
        .dispatch("auth/updateUserInfo", rewardAndFineInfo)
        .then(() => {
          console.log("signin and login succeeded.");
          let updateSuccessMessage = "ご褒美と罰金の設定を更新しました";
          this.$store.dispatch("flashMessage/setSuccessMessage", {
            messages: [updateSuccessMessage],
          });
          const next = "/";
          this.$router.replace(next);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
  computed: {
    threshouldRewardScore() {
      return this.$store.state.reward.threshouldRewardScore;
    },
    threshouldFineScore() {
      return this.$store.state.reward.threshouldFineScore;
    },
    amountOfReward() {
      return this.$store.state.reward.amountOfReward;
    },
    amountOfFine() {
      return this.$store.state.reward.amountOfFine;
    },
  },
};
</script>
