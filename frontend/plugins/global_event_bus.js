import Vue from 'vue'
export default function({ app, store }) {
  app.$bus = new Vue()
  if (store) store.$bus = app.$bus
}
