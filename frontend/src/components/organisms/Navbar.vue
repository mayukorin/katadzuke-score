<template>
  <nav>
    <v-app-bar app color="primary">
      <v-app-bar-nav-icon
        class="white--text"
        @click.stop="drawer = !drawer"
      ></v-app-bar-nav-icon>
      <v-toolbar-title class="text-uppercase white--text">
        <span class="font-weight-light">KDS</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn text v-bind="attrs" v-on="on" color="white">
            <v-icon left>mdi-chevron-down</v-icon>
            <span>Menu</span>
          </v-btn>
        </template>
        <v-list v-if="isLoggedIn"> </v-list>
        <v-list v-else> </v-list>
      </v-menu>
      <v-btn v-if="isLoggedIn" text color="white">
        <span>ログアウト</span>
        <v-icon right>mdi-exit-to-app</v-icon>
      </v-btn>
      <v-btn v-else text color="white">
        <span>ログイン</span>
        <v-icon right>mdi-exit-to-app</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer app v-model="drawer">
      <v-list v-if="isLoggedIn"> </v-list>
      <v-list v-else> </v-list>
    </v-navigation-drawer>
  </nav>
</template>
<script>
// import Appbar from "@/components/organisms/Appbar";

export default {
  name: "NavBar",
  data() {
    return {
      drawer: false,
    };
  },
  computed: {
    isLoggedIn() {
      return false;
    },
  },
};
</script>
