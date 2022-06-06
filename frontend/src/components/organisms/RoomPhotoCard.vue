<template>
  <div>
    <v-carousel v-model="photoIndex" class="my-4" :height="cardHeight + 60">
      <v-carousel-item>
        <div ref="roomPhotoCard0" class="ok">
          <v-card height="100%" flat>
            <div>
              <v-card-title class="text-h6 mt-2 mx-2" @click="search()">
                6/2 (木)
              </v-card-title>
              <v-card-text class="text-h5">
                <v-progress-circular
                  indeterminate
                  color="primary"
                ></v-progress-circular>
                点
              </v-card-text>
              <input
                style="display: none"
                ref="input"
                type="file"
                @change="selectedFile()"
              />
              <FloatingActionButton @click="handleClick()" :smallFlag="true">
                <v-icon dark> mdi-camera </v-icon>
                <span class="ml-1"> 部屋の写真変更 </span>
              </FloatingActionButton>
            </div>
            <div class="text-center aspect d-flex align-center justify-center">
              <v-progress-circular
                indeterminate
                color="primary"
                size="70"
              ></v-progress-circular>
            </div>
          </v-card>
        </div>
      </v-carousel-item>
      <v-carousel-item>
        <div ref="roomPhotoCard1" class="ok">
          <v-card height="100%">
            <div>
              <v-card-title class="text-h6 mt-2 mx-2" @click="search()">
                6/2 (木)
              </v-card-title>
              <v-card-text class="text-h5"> 100点 </v-card-text>
              <FloatingActionButton @click="handleClick()" :smallFlag="true">
                <v-icon dark> mdi-cloud-upload </v-icon>
                部屋の写真をアップロード
              </FloatingActionButton>
            </div>
            <v-img :src="url1" aspect-ratio="0.7" contain class="top-0 mb-1" />
          </v-card>
        </div>
      </v-carousel-item>
    </v-carousel>
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
      url1: "https://cdn.vuetifyjs.com/images/cards/foster.jpg",
      url2: "https://cdn.vuetifyjs.com/images/cards/cooking.png",
      photoIndex: 0,
      cardHeight: 0,
      uploadingFlag: false,
    };
  },
  computed: {
    isLoggedIn() {
      return false;
    },
  },
  methods: {
    search() {
      console.log(this.$refs.roomPhotoCard2.getBoundingClientRect().height);
    },
    handleClick() {
      this.$refs.input.click();
    },
    async selectedFile() {
      if (!this.uploadingFlag) {
        this.uploadingFlag = true;
        console.log("selected file");
        let file = this.$refs.input.files[0];
        if (file != null) {
          console.log(file);
          let reader = new FileReader();
          reader.onload = (event) => {
            let base64Text = event.currentTarget.result;
            return this.$store
              .dispatch("roomPhotos/upload", { roomPhoto: base64Text })
              .finally(() => {
                this.uploadingFlag = false;
              });
          };
          reader.readAsDataURL(file);
        }
        this.uploadingFlag = true;
      }
    },
  },
  mounted() {
    this.observer = new ResizeObserver((entries) => {
      for (let entry of entries) {
        // index で
        console.log(entry);
        let height = entry.contentRect.height;
        console.log(height);
        // console.log(this.$refs.roomPhotoCard2.getBoundingClientRect().height);
        if (height != 0) {
          this.cardHeight = height;
        }
      }
    });
    this.observer.observe(this.$refs.roomPhotoCard0);
    // 表示されていないから無理っぽい．表示されてないときは，0になるっぽい．
    // this.observer.observe(this.$refs.roomPhotoCard2);
  },
  watch: {
    photoIndex: function (newIndex, preIndex) {
      (async () => {
        const sleep = (second) =>
          new Promise((resolve) => setTimeout(resolve, second * 1000));
        let nextRef = "roomPhotoCard" + newIndex;
        let preRef = "roomPhotoCard" + preIndex;
        this.observer.unobserve(this.$refs[preRef]);
        await sleep(1);
        this.observer.observe(this.$refs[nextRef]);
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
