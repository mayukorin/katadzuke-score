<template>
  <v-app :style="{ background: '#fafafa' }">
    <Navbar />
    <v-main class="mx-4 mt-4">
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import Navbar from "@/components/organisms/Navbar";
export default {
  name: "App",
  components: {
    Navbar,
  },
  data: () => ({
    //
  }),
};
</script>
