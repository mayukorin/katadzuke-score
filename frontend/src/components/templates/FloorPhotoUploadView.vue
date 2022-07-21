<template>
  <div id="login-view">
    <v-container class="my-5">
      <v-row justify="center">
        <v-col cols="11" md="8">
          <FloorPhotoUploadCard />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import FloorPhotoUploadCard from "@/components/organisms/FloorPhotoUploadCard";
export default {
  name: "FloorPhotoUploadView",
  components: {
    FloorPhotoUploadCard,
  },
};
</script>
