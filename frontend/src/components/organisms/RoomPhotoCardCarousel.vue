<template>
  <div>
    <v-carousel v-model="photoIndex" class="my-4" :height="cardHeight + 60">
      <RoomPhotoCard2
        v-for="(roomPhoto, index) in roomPhotos"
        :key="roomPhoto.pk"
        :room-photo="roomPhoto"
        :day-of-week="dayOfWeeks[index]"
        ref="roomPhotoCard"
      />
    </v-carousel>
  </div>
</template>
<script>
import ResizeObserver from "resize-observer-polyfill";
import RoomPhotoCard2 from "@/components/organisms/RoomPhotoCard2";

export default {
  name: "RoomPhotoCardCarousel",
  components: {
    RoomPhotoCard2,
  },
  data() {
    return {
      photoIndex: 0,
      cardHeight: 0,
      dayOfWeeks: ["月", "火", "水", "木", "金", "土", "日"],
    };
  },
  computed: {
    isSignIn() {
      return false;
    },
    roomPhotos() {
      return this.$store.state.roomPhotos.roomPhotos;
    },
  },
  created() {
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
      console.log(this.$refs.roomPhotoCard[this.photoIndex]);
      // VueComponent だと OUT
      this.observer.observe(this.$refs.roomPhotoCard[this.photoIndex]);
    });
  },
  watch: {
    photoIndex: function (newIndex, preIndex) {
      (async () => {
        const sleep = (second) =>
          new Promise((resolve) => setTimeout(resolve, second * 1000));
        this.observer.unobserve(this.$refs.roomPhotoCard[preIndex]);
        await sleep(1);
        this.observer.observe(this.$refs.roomPhotoCard[newIndex]);
      })();
    },
  },
};
</script>
