<template>
  <div class="outbox">
    <div class="container">
      <Header :application-version="applicationVersion"></Header>
      <InputForm></InputForm>
<!--      <InputForm @search-click="get_condition"></InputForm>-->
    </div>
    <p>※GoogleMap表示はまだ調整中。</p>
    <GoogleMap></GoogleMap>
    <Conditions></Conditions>
  </div>
</template>

<script>
import InputForm from './components/InputForm';
import Conditions from './components/Conditions';
import GoogleMap from './components/GoogleMap';

export default {
  data() {
    return {
      applicationVersion: 'Vue版',
      eventData: {
      }
    };
  },
  methods: {
    get_condition(){
      this.eventData = this.$store.state.input_form;
    },
  },
  components: {
    GoogleMap,
    InputForm,
    Conditions,
  },
}
</script>

<style scoped>
  .outbox {
    width: 1300px;
    margin: 0 auto;
  }

  .container {
    width: 1200px;
    background-color: aliceblue;
    margin: 0 auto;
    padding-left: 20px;
    padding-right: 20px;
    text-align: left;
  }
</style>

