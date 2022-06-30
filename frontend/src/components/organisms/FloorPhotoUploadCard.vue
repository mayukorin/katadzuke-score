<template>
  <v-card class="login-card px-3" v-show="createdDoneFlag">
    <v-card-title>
      <span class="headline">床の写真</span>
    </v-card-title>
    <v-card-text>
      ※片付け具合の採点に利用します
      <FloorPhotoUploadForm
        @upload-button-click="handleUpload"
        :is-loading="isLoading"
        :floor-photo-url="floorPhoto.photo_url"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import FloorPhotoUploadForm from "@/components/molecules/FloorPhotoUploadForm";
export default {
  name: "FloorPhotoUploadCard",
  components: {
    FloorPhotoUploadForm,
  },
  data() {
    return {
      isLoading: false,
      createdDoneFlag: false,
    };
  },
  methods: {
    handleUpload(base64FloorPhoto) {
      this.isLoading = true;
      return this.$store
        .dispatch("floorPhoto/uploadFloorPhoto", {
          floorPhotoBase64Content: base64FloorPhoto,
          floorPhotoPk: this.floorPhoto.pk,
        })
        .then(() => {
          let uploadSuccessMessage = "床の部屋の写真を変更しました";
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
    floorPhoto() {
      console.log("change");
      console.log(this.$store.state.floorPhoto.floorPhoto);
      return this.$store.state.floorPhoto.floorPhoto;
    },
  },
  created() {
    return this.$store.dispatch("floorPhoto/get").then(() => {
      this.createdDoneFlag = true;
    });
  },
};
</script>
