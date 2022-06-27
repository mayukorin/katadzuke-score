<template>
  <div id="login-view">
    <v-container class="my-5">
      <v-row justify="center">
        <v-col cols="11" md="8">
          <RoomPhotoCardCarousel />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import RoomPhotoCardCarousel from "@/components/organisms/RoomPhotoCardCarousel";

export default {
  name: "HomeView",
  components: {
    RoomPhotoCardCarousel,
  },
};
</script>
