import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: "#00bcd4",
        primaryDark: "#0095a8",
        accent: "#ff9800",
      },
    },
    options: { customProperties: true, variations: false },
  },
});
