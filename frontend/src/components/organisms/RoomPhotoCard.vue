<template>
  <div>
    <v-card class="my-4">
      <v-card-title class="text-h6 mt-2 mx-2"> 6/2 (木) </v-card-title>
      <v-card-text class="text-h5"> 100点 </v-card-text>
      <v-img :src="url" contain />
    </v-card>
    <v-card class="my-4">
      <v-card-title class="text-h6 mt-2 mx-2"> 6/2 (木) </v-card-title>
      <v-card-text class="text-h5"> 100点 </v-card-text>
      <v-img :src="url" contain />
    </v-card>
  </div>
</template>
<script>
// import Appbar from "@/components/organisms/Appbar";

export default {
  name: "RoomPhotoCard",
  data() {
    return {
      drawer: false,
      url: "https://cdn.vuetifyjs.com/images/cards/foster.jpg",
    };
  },
  computed: {
    isLoggedIn() {
      return false;
    },
  },
};
</script>
