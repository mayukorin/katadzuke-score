<template>
  <div>
    <div v-show="isPageLoading" class="d-flex align-center justify-center">
      <v-progress-circular
        indeterminate
        color="primary"
        size="100"
        v-show="isPageLoading"
      ></v-progress-circular>
    </div>
    <div v-show="!isPageLoading">
      <v-carousel v-model="photoIndex" class="my-4" :height="cardHeight + 60">
        <v-carousel-item
          v-for="(roomPhoto, index) in roomPhotos"
          :key="roomPhoto.pk"
        >
          <div :ref="'roomPhotoCard' + index" class="ok">
            <v-card height="100%" flat>
              <div>
                <v-card-title class="text-h6 mt-2 mx-2" @click="search()">
                  {{ roomPhoto.filming_date }}({{ dayOfWeeks[index] }})
                </v-card-title>
                <v-card-text>
                  <div v-if="roomPhoto.photo_url == null">
                    片付け具合を採点するには部屋の写真を投稿してください
                  </div>
                  <div v-else class="text-h5">
                    <div v-show="!isUploading">
                      {{ roomPhoto.percent_of_floors }}点
                    </div>
                    <v-progress-circular
                      indeterminate
                      color="primary"
                      v-show="isUploading"
                    ></v-progress-circular>
                  </div>
                </v-card-text>
                <input
                  style="display: none"
                  ref="input"
                  type="file"
                  @change="selectedFile()"
                />
                <FloatingActionButton @click="handleClick()" :smallFlag="true">
                  <v-icon dark> mdi-camera </v-icon>
                  <span class="ml-1" v-if="roomPhoto.photo_url == null">
                    部屋の写真投稿
                  </span>
                  <span class="ml-1" v-else> 部屋の写真変更 </span>
                </FloatingActionButton>
              </div>
              <div
                class="text-center aspect d-flex align-center justify-center"
              >
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
      </v-carousel>
    </div>
  </div>
</template>
<script>
import ResizeObserver from "resize-observer-polyfill";
import FloatingActionButton from "@/components/atoms/FloatingActionButton.vue";

export default {
  name: "RoomPhotoCard",
  components: {
    FloatingActionButton,
  },
  data() {
    return {
      drawer: false,
      photoIndex: 0,
      cardHeight: 0,
      isUploading: false,
      isPageLoading: true,
      dayOfWeeks: ["月", "火", "水", "木", "金", "土", "日"],
    };
  },
  computed: {
    isSignIn() {
      return false;
    },
    roomPhotos() {
      console.log("change");
      return this.$store.state.roomPhotos.roomPhotos;
    },
  },
  methods: {
    search() {
      console.log(this.$refs.roomPhotoCard2.getBoundingClientRect().height);
    },
    getPhotoURL(photo_url) {
      if (photo_url == null) {
        // ToDo: 変数で表示
        return "https://res.cloudinary.com/dqyodswnq/image/upload/v1654651923/no_image_htu0nq.png";
      } else {
        return photo_url;
      }
    },
    handleClick() {
      this.$refs.input[0].click();
    },
    async selectedFile() {
      if (!this.isUploading) {
        this.isUploading = true;
        (async () => {
          const sleep = (second) =>
            new Promise((resolve) => setTimeout(resolve, second * 1000));
          await sleep(3);
        })();
        console.log("3s完了");
        let file = this.$refs.input[0].files[0];
        if (file != null) {
          console.log(file);
          let reader = new FileReader();
          reader.onload = (event) => {
            let base64Text = event.currentTarget.result;
            let score = 0;
            console.log("dispatch前");
            return this.$store
              .dispatch("roomPhotos/upload", {
                roomPhotoBase64Content: base64Text,
                roomPhotoPk: this.roomPhotos[this.photoIndex].pk,
              })
              .then((response) => {
                console.log("card側のresponse");
                console.log(response);
                score = response.percent_of_floors;
                return this.$store.dispatch("auth/getRewardThisMonth");
              })
              .then((response) => {
                let signInSuccessMessage = "片付け具合は" + score + "点です\n";
                if (response.amount_of_money < 0) {
                  signInSuccessMessage +=
                    "現時点で今月の罰金は" +
                    -1 * response.amount_of_money +
                    "円です";
                } else {
                  signInSuccessMessage +=
                    "現時点で今月のご褒美は" +
                    response.amount_of_money +
                    "円です";
                }
                this.$store.dispatch("flashMessage/setSuccessMessage", {
                  messages: [signInSuccessMessage],
                });
              })
              .finally(() => {
                console.log("final");
                this.isUploading = false;
              });
          };
          reader.readAsDataURL(file);
        } else {
          this.isUploading = false;
        }
      }
    },
  },
  created() {
    console.log("created");
    this.$store.dispatch("roomPhotos/list").then(() => {
      this.observer = new ResizeObserver((entries) => {
        for (let entry of entries) {
          let height = entry.contentRect.height;
          if (height != 0) {
            this.cardHeight = height;
          }
        }
      });
      console.log(this.$refs);
      console.log(this.$refs.roomPhotoCard0);
      this.observer.observe(this.$refs.roomPhotoCard0[0]);
      this.isPageLoading = false;
    });
  },
  watch: {
    photoIndex: function (newIndex, preIndex) {
      (async () => {
        const sleep = (second) =>
          new Promise((resolve) => setTimeout(resolve, second * 1000));
        let nextRef = "roomPhotoCard" + newIndex;
        let preRef = "roomPhotoCard" + preIndex;
        this.observer.unobserve(this.$refs[preRef][0]);
        await sleep(1);
        this.observer.observe(this.$refs[nextRef][0]);
      })();
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
