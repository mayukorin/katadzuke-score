<template>
  <div>
    <input
      style="display: none"
      ref="input"
      type="file"
      @change="selectedFile"
    />
    <FloatingActionButton @click="handleClick" :smallFlag="true">
      <v-icon dark> mdi-camera </v-icon>
      <span class="ml-1"> <slot /> </span>
    </FloatingActionButton>
  </div>
</template>
<script>
import FloatingActionButton from "@/components/atoms/FloatingActionButton.vue";

export default {
  name: "RoomPhotoUploadButton",
  components: {
    FloatingActionButton,
  },
  props: {
    isLoading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      isUploading: false,
      editedFullScoreRoomPhotoUrl: this.fullScoreRoomPhotoUrl,
      base64FullScoreRoomPhoto: "",
    };
  },
  methods: {
    handleClick() {
      this.$refs.input.click();
    },
    async selectedFile() {
      let file = this.$refs.input.files[0];
      if (file != null) {
        this.$emit("select-file", file);
        /*
        console.log(file);
        let reader = new FileReader();
        reader.onload = (event) => {
          this.base64FullScoreRoomPhoto = event.currentTarget.result;
          this.editedFullScoreRoomPhotoUrl = URL.createObjectURL(file);
        };
        reader.readAsDataURL(file);
        */
      }
    },
  },
};
</script>
