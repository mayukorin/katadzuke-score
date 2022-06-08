<template>
  <v-container class="mx-4">
    <v-row justify="center">
      <v-col cols="9" md="4">
        <RoomPhotoCard />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import RoomPhotoCard from "@/components/organisms/RoomPhotoCard";

export default {
  name: "HelloWorld",
  components: {
    RoomPhotoCard,
  },
  data: () => ({
    drawer: false,
  }),
};
</script>
