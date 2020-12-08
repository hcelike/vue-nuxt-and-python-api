<template>
    <nuxt-child/>
</template>

<script>

export default {
  layout: 'dashboard',
  middleware: ['auth', 'confirm'],
  components: {
  },
  data() {
    return {
    }
  },
  methods: {
    createSocket(){
      this.socket = this.$nuxtSocket({
        channel: '/',
        emitTimeout: 100,
        reconnection: true,
        forceNew: true,
      })
      this.socket
        .on('connect', (msg, cb) => {
          this.$store.commit('removeSnackBar');
        })
      this.socket
        .on('frontend_position', (msg, cb) => {
          this.$store.commit("setPositionsLastUpdated", new Date())
          console.log('POSITIONS from websocket', msg)
          this.$store.commit("setPositions", msg); 
          if (!this.$store.getters.isBrokerageConnected) {
            this.$store.dispatch('getBrokerageConnection');
          }
        })
      this.socket
        .on('frontend_alerts', (msg, cb) => {
          this.$store.commit("setAlerts", msg); 
          console.log("frontend_alert", msg);
        })
      this.socket
        .on('frontend_alert_events', (msg, cb) => {
          console.log("frontend_alert_events", msg);
          this.$store.commit("setAlertEvents", msg); 
        })
      this.socket
        .on('frontend_alert_event', (msg, cb) => {
          console.log("frontend_alert_event", msg);
          this.$store.dispatch('playAlertSound', msg);
        })
      this.socket
        .on('disconnect', (msg, cb) => {
          console.log("Disconnected...");
          this.$store.commit('showSnackBar', "Position feed disconnected");
          this.createSocket();  
        })
     },
  },
  beforeDestroy () {
  },
  mounted() {
    this.createSocket();
    this.$store.dispatch('getBrokerageConnection');
  },
}
</script>
