<template>
    <div id="map">
        <GmapMap :center="center" :zoom="zoom" style="width: 100%; height: 100%;">
            <GmapMarker v-for="(m,id) in marker_items"
                        :position="m.position"
                        :title="m.title"
                        :clickable="true" :draggable="false" :key="id"></GmapMarker>
        </GmapMap>
    </div>
</template>
<script>
  export default {
    data () {
      return {
        center: this.$store.state.location,
        zoom: 14,
        marker_items: [
          /* sample */
          {position: {lat: 35.71, lng: 139.72}, title: 'marker_1'},
          {position: {lat: 35.72, lng: 139.73}, title: 'marker_2'},
          {position: {lat: 35.70, lng: 139.71}, title: 'marker_3'},
          {position: {lat: 35.71, lng: 139.70}, title: 'marker_4'}
        ]
      }
    }
  }
</script>

