module.exports = {
  plugins: ["cypress"],
  env: {
    mocha: true,
    "cypress/globals": true,
  },
  rules: {
    strict: "off",
    'vue/multi-word-component-names': [
      'error',
      {
          ignores: ['default'],
      },
    ],
  },
};
