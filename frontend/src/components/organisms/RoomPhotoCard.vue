<template>
  <div>
    <v-carousel-item>
      <div :ref="'roomPhotoCard' + index">
        <v-card height="100%" flat>
          <div>
            <v-card-title class="text-h6 mt-2 mx-2">
              {{ roomPhoto.filming_date }}({{ dayOfWeek }})
            </v-card-title>
            <v-card-text>
              <div v-if="roomPhoto.photo_url == null">
                片付け具合を採点するには部屋の写真を投稿してください
              </div>
              <div v-else class="text-h5">
                <div v-show="!isUploading">
                  {{ roomPhoto.katadzuke_score }}点
                </div>
                <v-progress-circular
                  indeterminate
                  color="primary"
                  v-show="isUploading"
                ></v-progress-circular>
              </div>
            </v-card-text>
            <RoomPhotoUploadButton @select-file="selectedFile">
              <span v-if="roomPhoto.photo_url === null">部屋の写真投稿</span>
              <span v-else>部屋の写真変更</span>
            </RoomPhotoUploadButton>
          </div>
          <div class="text-center aspect d-flex align-center justify-center">
            <v-img
              :src="getPhotoURL(roomPhoto.photo_url)"
              aspect-ratio="0.7"
              contain
              class="top-0 mb-1"
              v-show="!isUploading"
            />
            <v-progress-circular
              indeterminate
              color="primary"
              size="70"
              v-show="isUploading"
            ></v-progress-circular>
          </div>
        </v-card>
      </div>
    </v-carousel-item>
  </div>
</template>
<script>
import RoomPhotoUploadButton from "@/components/molecules/RoomPhotoUploadButton.vue";

export default {
  name: "RoomPhotoCard",
  components: {
    RoomPhotoUploadButton,
  },
  props: {
    roomPhoto: {
      type: Object,
      defualt: null,
    },
    dayOfWeek: {
      type: String,
      defualt: "",
    },
    index: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      isUploading: false,
    };
  },
  created() {
    this.observer = new ResizeObserver((entries) => {
      for (let entry of entries) {
        let height = entry.contentRect.height;
        if (height != 0) {
          this.$emit("change-card-height", height);
        }
      }
    });
  },
  methods: {
    observeCard() {
      let ref = "roomPhotoCard" + this.index;
      this.observer.observe(this.$refs[ref]);
    },
    unObserveCard() {
      let ref = "roomPhotoCard" + this.index;
      this.observer.unobserve(this.$refs[ref]);
    },
    getPhotoURL(photo_url) {
      if (photo_url == null) {
        // TODO: 変数で表示
        return "https://res.cloudinary.com/dqyodswnq/image/upload/v1654651923/no_image_htu0nq.png";
      } else {
        return photo_url;
      }
    },
    handleClick() {
      this.$refs.input[0].click();
    },
    selectedFile(file) {
      if (!this.isUploading) {
        this.isUploading = true;
        if (file != null) {
          console.log(file);
          let reader = new FileReader();
          let prevRoomPhotoScore = this.roomPhoto.katadzuke_score;
          console.log("prev");
          console.log(prevRoomPhotoScore);
          reader.onload = (event) => {
            let base64Text = event.currentTarget.result;
            this.$store
              .dispatch("roomPhotos/upload", {
                roomPhotoBase64Content: base64Text,
                roomPhotoPk: this.roomPhoto.pk,
              })
              .then((response) => {
                return this.$store.dispatch(
                  "reward/updateAmountOfRewardThisMonth",
                  {
                    prevRoomPhotoScore: prevRoomPhotoScore,
                    newRoomPhotoScore: response.katadzuke_score,
                  }
                );
              })
              .finally(() => {
                console.log("final");
                this.isUploading = false;
              });
          };
          reader.readAsDataURL(file);
        }
      }
    },
  },
};
</script>
<style scoped>
.top-0 {
  margin-top: 0px !important;
}

.aspect {
  aspect-ratio: 7 / 10;
}
</style>
