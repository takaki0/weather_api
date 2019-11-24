<template>
  <div>
    <table class="conditions_table">
      <thead>
        <tr>
          <td>日付</td>
          <td>最高気温</td>
          <td>最低気温</td>
          <td>雲量</td>
          <td>湿度</td>
          <td>降水確率</td>
          <td>気圧</td>
          <td>オゾン指数</td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="condition in conditions" :key="condition.date">
          <td>{{ condition.date }}</td>
          <td>{{ condition.temperatureMax }}</td>
          <td>{{ condition.temperatureMin }}</td>
          <td>{{ condition.cloudCover }}</td>
          <td>{{ condition.humidity }}</td>
          <td>{{ condition.precipProbability }}</td>
          <td>{{ condition.pressure }}</td>
          <td>{{ condition.ozone }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  export default {
    // props: ["conditions"],
    computed: {
      conditions(){
        return this.$store.state.conditions;
      }
    },
  }
</script>

<style scoped>
  .conditions_table > thead > tr > td {
    font-size: 16px;
    font-weight: bold;
    width: 140px;
  }
</style>
