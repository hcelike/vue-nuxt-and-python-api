export const state = () => ({
  publicGlobals: {},
  brokerageAccountIds: [],
  snackbar: true,
  snackbar_text: null,
  snackbar_timeout: 5000,
  positionsLastUpdated: null,
  currentDate: new Date(),
  brokerage_connection: {ib_username: null, status: null},
  alerts: [
  ],
  alert_events: [
  ],
  positions: [
  ],
})

export const mutations = {
  storePublicGlobals(state, publicGlobals) {
    state.publicGlobals = publicGlobals;
  },
  setBrokerageAccountIds(state, value) {
    state.brokerageAccountIds = value;
  },
  setCurrentDate(state, date) { 
    state.currentDate = date;
  },
  setAlerts(state, alerts) {
    state.alerts = alerts
  },
  setAlertEvents(state, alert_events) {
    state.alert_events = alert_events
  },
  setPositionsLastUpdated(state, data) {
    state.positionsLastUpdated = data
  },
  setPositions(state, positions) {
     if (positions !== undefined && positions !== null) {
       console.log('setting', positions);
       state.positions = positions 
       if ( positions.length > 0 && state.brokerageAccountIds.length == 0) {
         state.brokerageAccountIds = positions[0].account_id;
       }
     } else {
        console.log('NOT setting', positions);
     }
  },
  setBrokerageConnection(state, brokerage_connection) {
    state.brokerage_connection = brokerage_connection
  },
  showSnackBar(state, text) {
    state.snackbar = true;
    state.snackbar_text = text;
  },
  removeSnackBar(state) {
    state.snackbar = false;
    state.snackbar_text = null;
  }
}


export const getters = {
  isBrokerageConnected(state, getters) {
    const status = state.brokerage_connection.status;
    if (status && status == 'CONNECTED') {
      return true;
    }
    return false;
  },
  availableBrokerageAccountIds(state, getters) {
     let ids = []
     if ( state.positions ) {
       ids = state.positions.map(d => d.account_id);
       ids = [...new Set(ids)];
     } 
     return ids;
  },
  secondsSincePositionsLastUpdated(state, getters) {
    let now = state.currentDate;
    if (state.positionsLastUpdated) {
      let difference = now.getTime() - state.positionsLastUpdated.getTime();
      let seconds = Math.abs(difference)/1000;
      return seconds;
    }
    return null;
  },
  shouldGetBrokerageConnection(state, getters) {
    if (state.brokerage_connection.status == "CONNECTING") {
      return true;
    }
    return false;
  },
  isTradingDay(state, getters) {
    if(state.currentDate.getDay() == 6 || state.currentDate.getDay() == 0) {
      return false
    }
    return true;
  },
  hasAlertSet: (state) => (position) => {
    const alertIds = state.alerts.filter(d => d.is_open).map(d => d.position.id);
    return alertIds.includes(position.id);
  },
  hasAnyAlertSet: (state, getters) => (positions) => {
    for (let position of positions) {
      if (getters.hasAlertSet(position)) {
        return true;
      }
    }
    return false;
  },
  selectedPositions(state, getters) {
    let positions = state.positions;
    if (state.brokerageAccountIds.length > 0) {
      positions = positions.filter(d => state.brokerageAccountIds.includes(d.account_id));
    } 
    return positions;
  },
  selectedAlerts(state, getters) {
    let alerts = state.alerts;
    if (state.brokerageAccountIds.length > 0) {
      alerts = alerts.filter(d => state.brokerageAccountIds.includes(d.position.account_id));
    } 
    return alerts;
  },
  selectedAlertEvents(state, getters) {
    let alert_events = state.alert_events;
    if (state.brokerageAccountIds.length > 0) {
      alert_events = alert_events.filter(d => state.brokerageAccountIds.includes(d.position.account_id));
    } 
    return alert_events;
  },
}

export const actions = {
  async nuxtServerInit({ dispatch, commit }, { req }) {
    // if you dont catch this exception the whole app wont load 
    try {
       await dispatch('getPublicGlobals')
    } catch(e){
       console.log(e);
    }
  },
  async nuxtClientInit({ dispatch, commit }, { req }) {
    // if you dont catch this exception the whole app wont load 
    try {
       await dispatch('getPublicGlobals')
    } catch(e){
       console.log(e);
    }
  },
  async getPublicGlobals({ commit }) {
    let data = await this.$axios.$get('/v1/public_globals')
    commit("storePublicGlobals", data);
  },
  addAlert({ commit, dispatch }, alert) {
    this.$axios.$post('/v1/alerts/', alert) 
      .then(resp => {
        dispatch('getAlerts')
        commit('showSnackBar', "Alert Created")
      })
      .catch(error => {
      })
  },
  connectBrokerage({ commit, dispatch }, form) {
    new Promise((resolve, reject) => {
      this.$axios.$post('/v1/brokerage_connection', form) 
        .then(response => {
          dispatch('getBrokerageConnection')
          resolve(response)
        })
        .catch(error => {
          let resp = error.response.data
          commit('showSnackBar', `Failed to connect brokerage: ${resp}`)
          reject(resp)
        })
      })
  },
  disconnectBrokerage({ commit, dispatch }) {
    this.$axios.$delete(`/v1/brokerage_connection`)
      .then(resp => {
        dispatch('getBrokerageConnection')
      })
      .catch(error => {
      })
  },
  getBrokerageConnection({ state, commit, getters }) {
    this.$axios.$get('/v1/brokerage_connection', { progress: false })
      .then(response => {
        commit('setBrokerageConnection', response);
      })
      .catch(error => {
      })
  },
  editAlert({ commit, dispatch }, alert) {
    this.$axios.$put(`/v1/alerts/${alert.id}`, alert) 
      .then(resp => {
        dispatch('getAlerts')
      })
      .catch(error => {
      })
  },
  deleteAlert({ commit, dispatch }, alert) {
    this.$axios.$delete(`/v1/alerts/${alert.id}`)
      .then(resp => {
        dispatch('getAlerts')
      })
      .catch(error => {
      })
  },
  getAlerts({ state, commit }) {
    this.$axios.$get('/v1/alerts')
      .then(response => {
        commit('setAlerts', response.data);
      })
      .catch(error => {
      })
  },
  getAlertEvents({ state, commit }) {
    this.$axios.$get('/v1/alert_events')
      .then(response => {
        commit('setAlertEvents', response.data);
      })
      .catch(error => {
      })
  },
  getPositions({ state, commit }) {
    this.$axios.$get('/v1/positions')
      .then(response => {
        console.log('POSITIONS from GET', response)
        console.log('POSITIONS from GET', response.data)
        commit('setPositions', response.data);
      })
      .catch(error => {
      })
  },
  playAlertSound({ state, commit}, alert_event) {
    try {
      if (state.auth.user.enable_sound_alerts) {
        let sound  = new Audio("https://tonejs.github.io/audio/berklee/gong_1.mp3")
        sound.play();
      }
      if (state.auth.user.enable_voice_alerts) {
        let msg = new SpeechSynthesisUtterance();
        msg.text = alert_event.alert.message;
        window.speechSynthesis.speak(msg);
      }
    } 
    catch(e) {
      console.log('FAILED to play audio:', e)
    }
  },
}
export const strict = false;

