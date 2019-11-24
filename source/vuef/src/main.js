import Vue from 'vue'
import App from './App.vue'
import Header from './components/Header';
import store from './store';
import * as VueGoogleMaps from 'vue2-google-maps'


Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyCbrRVCZafZLP2hQntNvKT6BdOEJMevF8o',
    libraries: 'places',
  },
});

Vue.config.productionTip = false;

//common component
Vue.component("Header", Header);

// common filter
Vue.filter("numFormat", function (value) {
  return Number(value).toLocaleString( undefined, { maximumFractionDigits: 20 });
});

//common directive
Vue.directive("github", function(el, binding){
  el.style.Color = binding.value.color;
  el.href = 'https://github.com/takaki0/weather_api';
  el.target = '_blank';
  if (binding.arg === 'none') {
    el.style.borderStyle = "none";
  }
  if (binding.modifiers.round) {
    el.style.borderRadius = "0.4rem";
  }
  if (binding.modifiers.shadow) {
    el.style.boxShadow = "0 2px 5px";
  }
  if (binding.modifiers.padding) {
    el.style.padding = "2px";
  }
});

new Vue({
  store,
  render: h => h(App),
}).$mount('#app');
