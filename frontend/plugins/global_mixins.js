import Mixin from '~/mixins/mixins.js';
import Vue from 'vue';

if (!Vue.__my_mixin__) {
  Vue.__my__mixin__ = true
  console.log('adding mixins...');
  Vue.mixin(Mixin) // Set up your mixin then
}
