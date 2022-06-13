<template>
  <v-btn
    :text="textFlag"
    :class="classString"
    :color="colorString"
    @click="handleClick"
    depressed
    :loading="isLoading"
    :small="smallFlag"
    :disabled="disableFlag"
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
      default: false,
    },
    classString: {
      type: String,
      default: "mt-3 mx-auto mb-3",
    },
    colorString: {
      type: String,
      default: "primary",
    },
    smallFlag: {
      type: Boolean,
      default: false,
    },
    disableFlag: {
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
