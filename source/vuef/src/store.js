import Vue from 'vue';
import Vuex from 'vuex';
import Axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    input_form: {
      city_name: '大阪',
      from_date: '2019-11-21',
      to_date: '2019-11-25',
    },
    location: { //初期表示：東京
      lat: 35.6585805,
      lng: 139.7454329,
    },
    conditions : [],
    error_message: '',
    http_status: '',
  },
  getters: {
    getErrorMessage: state => {
      if (state.http_status && state.http_status != '200'){
        return state.error_message + '(' + state.http_status + ')';
      }else{
        return '';
      }
    },
  },
  mutations: {
    set_input_form(state, form_values){
      state.input_form = form_values;
    },
    set_conditions(state, values){
      state.conditions = values.conditions;
      state.location = values.location;
      state.error_message = values.message;
      state.http_status = values.status;
    },
    set_error_message(state, values){
      state.error_message = values.message;
      state.http_status = values.status;
    },
  },
  actions: {
    set_input_form({ commit }, form_values){
      commit('set_input_form', form_values);

      //call python API
      const WEATHER_API_ENDPOINT = 'weather/get_condition_by_city/dc5c49bc74131f57699d93c3e961d86a';

      Axios
        .get(WEATHER_API_ENDPOINT, { params: form_values })
        .then((result) => {
          const status = result.data.status;
          const message = result.data.message;
          //取得失敗
          if (status !== 200) {
            commit('set_error_message', { status, message});
            return;
          }
          //取得成功
          const conditions = result.data.weather_conditions;
          const latlng = result.data.location;
          const location = { lat: latlng.latitude, lng: latlng.longitude };
          commit('set_conditions', { status, message, conditions, location });
        })
        .catch(() => {
          //通信エラーなど
          const status = 500;
          const message = 'url error';
          commit('set_error_message', { status, message});
        });
    },
  }
});

