const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: ["vuetify"],
  outputDir: "../static",
  indexPath: "../templates/index.html",
  publicPath: process.env.NODE_ENV === "production" ? "/static" : "/",
  configureWebpack: {
    watchOptions: {
      aggregateTimeout: 300,
      poll: 1000,
    },
  },
});
