<template>
  <v-container class="mx-4">
    <v-row justify="center">
      <v-col cols="9" md="4">
        <RoomPhotoCardCarousel />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import RoomPhotoCardCarousel from "@/components/organisms/RoomPhotoCardCarousel";

export default {
  name: "HelloWorld",
  components: {
    RoomPhotoCardCarousel,
  },
  data: () => ({
    drawer: false,
  }),
};
</script>
