import Vue from 'vue'

// Allows global use of these methods
Vue.mixin({
  methods: {
    currency(num, n=2) {
      let x = null;
      let re = "\\d(?=(\\d{" + (x || 3) + "})+" + (n > 0 ? "\\." : "$") + ")";
      try {
          num = parseFloat(num);
      } catch(e){
      }
      try {
          return (
          "$" + num.toFixed(Math.max(0, ~~n)).replace(new RegExp(re, "g"), "$&,")
          );
      } catch (e) {
          return num;
      }
    },
  }
})
