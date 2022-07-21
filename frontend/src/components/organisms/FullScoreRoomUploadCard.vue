<template>
  <v-card class="login-card px-3">
    <v-card-title>
      <span class="headline">100点満点の部屋</span>
    </v-card-title>
    <v-card-text>
      ※片付け具合の採点に利用します
      <FullScoreRoomUploadForm
        @upload-button-click="handleUpload"
        :is-loading="isLoading"
        :full-score-room-photo-url="fullScoreRoomPhoto.photo_url"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import FullScoreRoomUploadForm from "@/components/molecules/FullScoreRoomUploadForm";
export default {
  name: "FullScoreRoomUploadCard",
  components: {
    FullScoreRoomUploadForm,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  methods: {
    handleUpload(base64FullScoreRoomPhoto) {
      this.isLoading = true;
      return this.$store
        .dispatch("roomPhotos/uploadFullScoreRoomPhoto", {
          roomPhotoBase64Content: base64FullScoreRoomPhoto,
          roomPhotoPk: this.fullScoreRoomPhoto.pk,
        })
        .then(() => {
          let uploadSuccessMessage = "100点満点の部屋の写真を変更しました";
          this.$store.dispatch("flashMessage/setSuccessMessage", {
            messages: [uploadSuccessMessage],
          });
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
  computed: {
    fullScoreRoomPhoto() {
      console.log("change");
      console.log(this.$store.state.roomPhotos.fullScoreRoomPhoto);
      return this.$store.state.roomPhotos.fullScoreRoomPhoto;
    },
  },
};
</script>
