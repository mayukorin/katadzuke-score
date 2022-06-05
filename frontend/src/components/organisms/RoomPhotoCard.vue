<template>
  <div>
    <v-carousel v-model="photoIndex" class="my-4" :height="cardHeight + 60">
      <v-carousel-item>
        <div ref="roomPhotoCard0" class="ok">
          <v-card height="100%">
            <div>
              <v-card-title class="text-h6 mt-2 mx-2" @click="search()">
                6/2 (木)
              </v-card-title>
              <v-card-text class="text-h5"> 100点 </v-card-text>
            </div>
            <v-img :src="url1" aspect-ratio="0.7" contain class="top-0 mb-1" />
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
            </div>
            <v-img :src="url1" aspect-ratio="0.7" contain class="top-0 mb-1" />
          </v-card>
        </div>
      </v-carousel-item>
    </v-carousel>
  </div>
</template>
<script>
// import Appbar from "@/components/organisms/Appbar";
import ResizeObserver from "resize-observer-polyfill";

export default {
  name: "RoomPhotoCard",
  data() {
    return {
      drawer: false,
      url1: "https://cdn.vuetifyjs.com/images/cards/foster.jpg",
      url2: "https://cdn.vuetifyjs.com/images/cards/cooking.png",
      photoIndex: 0,
      cardHeight: 0,
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
</style>
