<template>
  <v-btn
    rounded
    dark
    :text="textFlag"
    :class="classString"
    :color="colorString"
    @click="handleClick"
    :small="smallFlag"
  >
    <slot />
  </v-btn>
</template>
<script>
export default {
  name: "FloatingActionButton",
  props: {
    textFlag: {
      type: Boolean,
      default: false,
    },
    classString: {
      type: String,
      default: "accent mt-3 mx-auto mb-3",
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
