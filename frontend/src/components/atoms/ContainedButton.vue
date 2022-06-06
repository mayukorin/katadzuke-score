<template>
  <v-btn
    :text="textFlag"
    :class="classString"
    :color="colorString"
    @click="handleClick"
    depressed
    :loading="isLoading"
    :small="smallFlag"
  >
    <slot />
  </v-btn>
</template>
<script>
export default {
  name: "ContainedButton",
  props: {
    isLoading: {
      type: Boolean,
      default: false,
    },
    textFlag: {
      type: Boolean,
      default: true,
    },
    classString: {
      type: String,
      default: "primary mt-3 mx-auto mb-3",
    },
    colorString: {
      type: String,
      default: "",
    },
    smallFlag: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    handleClick(ev) {
      this.$emit("click", ev);
    },
  },
};
</script>
