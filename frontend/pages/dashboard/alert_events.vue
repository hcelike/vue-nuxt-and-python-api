<template>
  <v-layout
    column
    justify-center
  >
    <v-flex
      xs12
      sm12
      md12
    >
      <v-data-table
        :headers="headers"
        :items="$store.getters.selectedAlertEvents"
        :items-per-page="50"
        group-by="position.symbol"
        dense
        class="elevation-1"
      >
      <template v-slot:group.header="{ items, isOpen, toggle}">
        <th 
            class="text-xs-right"
            :colspan="headers.length"
          > 
          <v-icon @click="toggle"
            >{{ isOpen ? 'mdi-minus' : 'mdi-plus' }}
          </v-icon>
           {{ items[0].position.symbol}}
        </th>
      </template>
      <template v-slot:item.position="{ item }"> 
         <span style='margin-left:2rem'>
            {{ formatInstrument(item.position) }}
         </span>
      </template>
      <template v-slot:item.created_date="{ item }"> 
        {{ formatDateLong(item.created_date) }}
      </template>
      <template v-slot:item.value="{ item }"> 
         {{ toCurrency(item.value) }}
      </template>
      </v-data-table>
    </v-flex>
  </v-layout>
</template>

<script>

export default {
  middleware: ['auth'],
  layout: 'dashboard',
  components: {
  },
  data(){
    return {
      headers: [
        { text: 'Position', value: 'position' },
        { text: 'Field', value: 'alert.field' },
        { text: 'Condition', value: 'alert.condition' },
        { text: 'Value', value: 'value' },
        { text: 'Created Date', value: 'created_date' },
      ],
    }
  },
  methods: {
  },
  mounted() {
    this.$store.dispatch('getAlertEvents');
  },
}
</script>
<style>
.v-row-group__header {
  background: inherit!important;
}
</style>
