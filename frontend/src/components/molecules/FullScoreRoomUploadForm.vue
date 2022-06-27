<template>
  <div>
    <v-form ref="form">
      <RoomPhotoUploadButton @select-file="selectedFile">
        100点満点の部屋の写真選択
      </RoomPhotoUploadButton>
      <br />
      <ContainedButton
        @click="handleUpload"
        :is-loading="isLoading"
        :disable-flag="base64FullScoreRoomPhoto === ''"
        >アップロード</ContainedButton
      >
    </v-form>
    現在の100点満点の部屋 <br />
    <v-img :src="editedFullScoreRoomPhotoUrl" aspect-ratio="0.7" contain />
  </div>
</template>

<script>
import ContainedButton from "@/components/atoms/ContainedButton";
import RoomPhotoUploadButton from "@/components/molecules/RoomPhotoUploadButton.vue";

export default {
  name: "FullScoreRoomUploadForm",
  components: {
    ContainedButton,
    RoomPhotoUploadButton,
  },
  props: {
    isLoading: {
      type: Boolean,
      default: false,
    },
    fullScoreRoomPhotoUrl: {
      type: String,
      default: "",
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
    handleUpload() {
      if (!this.isLoading) {
        this.$emit("upload-button-click", this.base64FullScoreRoomPhoto);
      }
    },
    selectedFile(file) {
      if (file != null) {
        console.log(file);
        let reader = new FileReader();
        reader.onload = (event) => {
          this.base64FullScoreRoomPhoto = event.currentTarget.result;
          this.editedFullScoreRoomPhotoUrl = URL.createObjectURL(file);
        };
        reader.readAsDataURL(file);
      }
    },
  },
};
</script>
