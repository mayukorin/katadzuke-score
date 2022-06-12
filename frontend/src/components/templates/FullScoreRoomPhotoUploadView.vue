<template>
  <div id="login-view">
    <v-container class="my-5">
      <v-row justify="center">
        <v-col cols="11" md="8">
          <FullScoreRoomUploadCard />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import FullScoreRoomUploadCard from "@/components/organisms/FullScoreRoomUploadCard";
export default {
  name: "FullScoreRoomPhotoUploadView",
  components: {
    FullScoreRoomUploadCard,
  },
};
</script>
