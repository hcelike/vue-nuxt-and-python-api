<template>
  <v-select
    :items="$store.getters.availableBrokerageAccountIds"
    label="Brokerage Account ID"
    v-model="brokerageAccountIds"
    placeholder='All Accounts'
    dense
    outlined
    style='font-size:10px'
  >
  </v-select>
</template>

<script>
export default {
  computed: {
    brokerageAccountIds: {
      get () {
        return this.$store.state.brokerageAccountIds;
      },
      set (value) {
        this.$store.commit('setBrokerageAccountIds', value)
      }
    }
  },
}
</script>

