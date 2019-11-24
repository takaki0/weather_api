<template>
  <div class="input-form">
      <label for="city_name">都市：</label>
      <input
              id="city_name"
              type="text"
              v-model.trim="form_data.city_name"
      />
      <label for="from_date">期間（開始日）：</label>
      <input
              id="from_date"
              type="text"
              v-model.trim="form_data.from_date"
      />
      <label for="to_date">〜（終了日）：</label>
      <input
              id="to_date"
              type="text"
              v-model.trim="form_data.to_date"
      />
      <button @click="search_click" class="search-button">検索</button>
      <br>
      <p class="result_message">{{ errorMessage }}</p>
  </div>
</template>

<script>
  export default {
    name: "InputForm",
    data() {
        return {
          form_data: {
            city_name: '東京',
            from_date: '2019-12-01',
            to_date: '2019-12-07',
          },
        }
    },
    computed: {
      errorMessage(){
        return this.$store.getters.getErrorMessage;
      }
    },
    methods: {
      search_click() {
        this.$store.dispatch('set_input_form', this.form_data);
        // this.$emit("search-click");
      },
    },
  }
</script>

<style scoped>
.result_message {
    font-size: 20px;
    color: #ff8877;
}

.input-form {
    margin: 0 auto;
    text-align: center;
}

input[type='text'] {
    font-size: 18px;
    padding: 3px;
}

#city_name {
    width: 250px;
    margin-right: 20px;
}

#from_date, #to_date {
    width: 150px;
    margin-right: 15px;
}

.search-button {
    -webkit-appearance: none;
    font-size: 18px;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-left: 5px;
}

</style>