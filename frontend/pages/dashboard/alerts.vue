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

    <template>
     <v-tabs v-model='activeTab'>
       <v-tab>Active</v-tab>
       <v-tab>Triggered</v-tab>
     </v-tabs>
   </template> 

     <alert-dialog :positions="$store.getters.selectedPositions" />

      <v-data-table
        :headers="headers"
        :items="alerts"
        group-by="position.symbol"
        :hide-default-footer="true"
        :disable-pagination='true'
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
      <template v-slot:item.value="{ item }"> 
         {{ toCurrency(item.value) }}
      </template>
      <template v-slot:item.expiration_date="{ item }"> 
        {{ item.expiration_date ? formatDate(item.expiration_date) : "Expire on close" }}
      </template>
       <template v-slot:item.actions="{ item }">
         <v-icon
           small
           class="mr-2"
           @click="editItem(item)"
         >
           mdi-pencil
         </v-icon>
         <v-icon
           small
           @click="deleteItem(item)"
         >
           mdi-delete
         </v-icon>
       </template>
      </v-data-table>
    </v-flex>
  </v-layout>
</template>

<script>
import AlertDialog from '~/components/AlertDialog.vue';

export default {
  middleware: ['auth'],
  layout: 'dashboard',
  components: {
    AlertDialog,
  },
  data(){
    return {
      dialog: false,
      activeTab: 0,
      headers: [
        { text: 'Position', value: 'position' },
        { text: 'Symbol', value: 'position.symbol', align: ' d-none' },
        { text: 'Field', value: 'field' },
        { text: 'Condition', value: 'condition' },
        { text: 'Value', value: 'value' },
        { text: 'Expiration Date', value: 'expiration_date' },
        { text: 'Alert Types', value: 'alert_types' },
        { text: 'Actions', value: 'actions', sortable: false }
      ],
    }
  },
  computed: {
    alerts() {
      let alerts = this.$store.getters.selectedAlerts;
      if (this.activeTab == 0) {
        alerts = alerts.filter(d => d.is_open);     
      } 
      else if (this.activeTab == 1) {
        alerts = alerts.filter(d => !d.is_open);     
      }
      return alerts;
    },
  },
  methods: {
    editItem(alert) {
      this.$store.$bus.$emit('editItem', alert, alert.position)
    },
    deleteItem (item) {
      confirm('Are you sure you want to delete this alert?') && this.$store.dispatch('deleteAlert', item)
    },
  },
  mounted() {
    this.$store.dispatch('getAlerts');
    this.$store.dispatch('getPositions');
  },
}
</script>
<style>
.v-row-group__header {
  background: inherit!important;
}
</style>
