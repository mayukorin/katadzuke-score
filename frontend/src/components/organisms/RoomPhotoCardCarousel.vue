<template>
  <div>
    <v-carousel v-model="photoIndex" class="my-4" :height="cardHeight + 60">
      <RoomPhotoCard
        v-for="(roomPhoto, index) in roomPhotos"
        :key="roomPhoto.pk"
        :room-photo="roomPhoto"
        :day-of-week="dayOfWeeks[index]"
        @change-card-height="setCardHeight"
        ref="roomPhotoCard"
      />
    </v-carousel>
  </div>
</template>
<script>
import ResizeObserver from "resize-observer-polyfill";
import RoomPhotoCard from "@/components/organisms/RoomPhotoCard";

export default {
  name: "RoomPhotoCardCarousel",
  components: {
    RoomPhotoCard,
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
      console.log(this.$store.state.roomPhotos.fullScoreRoomPhotoURL);
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
      console.log("created");
      console.log(this.$refs.roomPhotoCard[0]);
      this.$refs.roomPhotoCard[0].observeCard();
    });
  },
  watch: {
    photoIndex: function (newIndex, preIndex) {
      (async () => {
        const sleep = (second) =>
          new Promise((resolve) => setTimeout(resolve, second * 1000));
        this.$refs.roomPhotoCard[preIndex].unObserveCard();
        await sleep(1);
        this.$refs.roomPhotoCard[newIndex].observeCard();
      })();
    },
  },
  methods: {
    setCardHeight(height) {
      this.cardHeight = height;
    },
  },
};
</script>
