import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import VueSession from 'vue-session'
import moment from 'moment'
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';



Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).calendar()
  }
})

Vue.filter('duration', function(value) {
  if (value) {
    var years = Math.floor(value/12);
    var months = value % 12;
    if(months == 0){
      return years+" Years"
    }
    return years+" Years and "+months +" Months"
  }
})

Vue.use(VueSweetalert2);
Vue.use(VueSession)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
