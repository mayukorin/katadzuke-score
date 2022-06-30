<template>
  <div>
    <v-form ref="form">
      <RoomPhotoUploadButton @select-file="selectedFile">
        床の写真選択
      </RoomPhotoUploadButton>
      <br />
      <ContainedButton
        @click="handleUpload"
        :is-loading="isLoading"
        :disable-flag="base64FloorPhoto === ''"
        >アップロード</ContainedButton
      >
    </v-form>
    現在の床の写真 <br />
    <v-img :src="editedfloorPhotoUrl" aspect-ratio="0.7" contain />
  </div>
</template>

<script>
import ContainedButton from "@/components/atoms/ContainedButton";
import RoomPhotoUploadButton from "@/components/molecules/RoomPhotoUploadButton.vue";

export default {
  name: "FloorPhotoUploadForm",
  components: {
    ContainedButton,
    RoomPhotoUploadButton,
  },
  props: {
    isLoading: {
      type: Boolean,
      default: false,
    },
    floorPhotoUrl: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      isUploading: false,
      editedfloorPhotoUrl: this.floorPhotoUrl,
      base64FloorPhoto: "",
    };
  },
  methods: {
    handleClick() {
      this.$refs.input.click();
    },
    handleUpload() {
      if (!this.isLoading) {
        this.$emit("upload-button-click", this.base64FloorPhoto);
      }
    },
    selectedFile(file) {
      if (file != null) {
        console.log(file);
        let reader = new FileReader();
        reader.onload = (event) => {
          this.base64FloorPhoto = event.currentTarget.result;
          this.editedfloorPhotoUrl = URL.createObjectURL(file);
        };
        reader.readAsDataURL(file);
      }
    },
  },
};
</script>
