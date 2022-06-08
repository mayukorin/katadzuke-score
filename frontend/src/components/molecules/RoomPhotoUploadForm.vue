<template>
  <v-form>
    <v-file-input label="部屋の写真" prepend-icon="mdi-camera"></v-file-input>
    <ContainedButton :is-loading="isLoading" @click="handleClick()">
      アップロード
      <v-icon right dark> mdi-cloud-upload </v-icon>
    </ContainedButton>
  </v-form>
</template>
<script>
import ContainedButton from "@/components/atoms/ContainedButton.vue";

export default {
  name: "RoomPhotoUploadForm",
  components: {
    ContainedButton,
  },
  props: {
    isLoading: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    handleClick() {
      this.$emit("upload-button-click");
    },
  },
};
</script>
