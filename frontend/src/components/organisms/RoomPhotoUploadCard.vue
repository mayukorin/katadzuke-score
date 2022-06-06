<template>
  <v-card>
    <v-card-title>
      <span class="headline">部屋の写真をアップロード</span>
    </v-card-title>
    <v-card-text>
      <RoomPhotoUploadForm
        @upload-button-click="handleUpload"
        :is-loading="isLoading"
      />
    </v-card-text>
  </v-card>
</template>
<script>
import RoomPhotoUploadForm from "@/components/molecules/RoomPhotoUploadForm";

export default {
  name: "RoomPhotoUploadCard",
  components: {
    RoomPhotoUploadForm,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  methods: {
    handleUpload: function () {
      this.isLoading = true;
      console.log("ok");
    },
  },
};
</script>
