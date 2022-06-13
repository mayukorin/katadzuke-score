<template>
  <div>
    <v-form ref="form">
      <v-container fluid>
        ご褒美の設定<br />
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="form.editedThreshouldRewardScore"
              label="ご褒美を上げる点数"
              value="70"
              suffix="点以上"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="form.editedAmountOfReward"
              label="ご褒美の金額"
              value="500"
              suffix="円"
            ></v-text-field>
          </v-col>
        </v-row>
        罰金の設定<br />
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="form.editedThreshouldFineScore"
              label="罰金となる点数"
              value="30"
              suffix="点以下"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="form.editedAmountOfFine"
              label="罰金の金額"
              value="500"
              suffix="円"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-container>
      <ContainedButton @click="handleUpdate" :is-loading="isLoading"
        >更新</ContainedButton
      >
    </v-form>
  </div>
</template>

<script>
import ContainedButton from "@/components/atoms/ContainedButton";

export default {
  name: "RewardAndFineUpdateForm",
  components: {
    ContainedButton,
  },
  props: {
    isLoading: {
      type: Boolean,
      default: false,
    },
    threshouldRewardScore: {
      type: Number,
      default: 0,
    },
    threshouldFineScore: {
      type: Number,
      default: 0,
    },
    amountOfReward: {
      type: Number,
      default: 0,
    },
    amountOfFine: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      isUploading: false,
      form: {
        editedThreshouldRewardScore: this.threshouldRewardScore,
        editedThreshouldFineScore: this.threshouldFineScore,
        editedAmountOfReward: this.amountOfReward,
        editedAmountOfFine: this.amountOfFine,
      },
    };
  },
  methods: {
    handleUpdate() {
      if (!this.isLoading) {
        this.$emit("update-button-click", {
          threshould_reward_score: this.form.editedThreshouldRewardScore,
          threshould_fine_score: this.form.editedThreshouldFineScore,
          amount_of_reward: this.form.editedAmountOfReward,
          amount_of_fine: this.form.editedAmountOfFine,
        });
      }
    },
  },
};
</script>
