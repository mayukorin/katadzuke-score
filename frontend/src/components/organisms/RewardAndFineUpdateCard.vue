<template>
  <v-card class="login-card px-3">
    <v-card-title>
      <span class="headline">ご褒美と罰金の設定</span>
    </v-card-title>
    <v-card-text>
      <RewardAndFineUpdateForm
        :is-loading="isLoading"
        :reward="reward"
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
      this.$store
        .dispatch("auth/updateUserInfo", rewardAndFineInfo)
        .then(() => {
          console.log("signin and login succeeded.");
          let updateSuccessMessage = "ご褒美と罰金の設定を更新しました";
          this.$store.dispatch("flashMessage/setSuccessMessage", {
            messages: [updateSuccessMessage],
          });
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
  // TODO: 一つにまとめる
  computed: {
    reward() {
      return this.$store.state.reward;
    },
  },
};
</script>
