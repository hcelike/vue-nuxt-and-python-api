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
      
     
      <alert-dialog :positions='$store.state.positions' />
      <v-data-table
        :headers="headers"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :items="filteredPositions"
        :disable-pagination='true'
        mobile-breakpoint="0"
        :hide-default-footer="true"
        group-by="symbol"
        ref='table'
        dense
        class="elevation-1"
      >

      <template v-slot:group.header="{ group, items, isOpen, toggle, headers}">
        <th  
            class="text-xs-right"
            colspan='2'
          > 
           <v-row dense @click='toggle'>
             <v-col :cols='$device.isDesktop ? 2 : 5'>
             <span>
                <span v-if='$device.isMobile && $store.getters.hasAnyAlertSet(items)'>
                   <v-icon style='font-size:15px'>mdi-bell-check</v-icon>
                </span>
                <span style='font-size: 1rem'>{{ items[0].symbol }}</span>
              </span>
             </v-col>
             <v-col v-if='$device.isMobile'>
               <p style='font-size: 1rem;margin-bottom:0px' class="text-right">
                 <span :class='`${pnlClass(aggregatePosition(items))}--text`'>
                     {{ toCurrency(underlyingPrice(items)) }} 
                 </span>
               </p>
             </v-col>
           </v-row>
        </th>
      <td v-if='$device.isDesktop'> 
        <span v-if='$store.getters.hasAlertSet(aggregatePosition(items))'>
           <v-icon style='font-size:15px'>mdi-bell-check</v-icon>
        </span>
      </td>
       <td v-if='$device.isDesktop' v-for="header in headers.slice(3, headers.length)">
         <template v-if='$store.state.publicGlobals.fields.includes(header.value)'>
           <div @contextmenu.prevent="handler" 
             @click='editItem(aggregatePosition(items), header.value)' 
             @click.right='editItem(aggregatePosition(items), header.value)' style='cursor:pointer'>
               <span v-if='aggregatePosition(items)[header.value] || header.value == "price"'>
                 <template v-if='header.value == "daily_pnl"'>
                   <span :class='`${pnlClass(aggregatePosition(items))}--text`' style='font-weight:600'>
                      {{ toCurrency(aggregatePosition(items)[header.value]) }}
                   </span>
                 </template>
                 <template v-else-if='header.value == "price"'>
                   <span style='font-weight:600'>
                     {{ toCurrency(underlyingPrice(items))}} 
                   </span>
                 </template>
                 <template v-else>
                   <span  style='font-weight:600'>
                     {{ toCurrency(aggregatePosition(items)[header.value]) }}
                   </span>
                 </template>
               </span>
               <span v-else>
                 -- 
               </span>
           </div> 
         </template>
       </td>
      </template>
      <template v-slot:item.alert_set="{ item }">
        <span v-if='$store.getters.hasAlertSet(item)'>
           <v-icon style='font-size:15px'>mdi-bell-check</v-icon>
        </span>
      </template>
      <template v-slot:item.instrument="{ item }">
        <v-row style='white-space: nowrap;'>
          <v-col>
            <span v-if='$device.isMobile && $store.getters.hasAlertSet(item)'>
               <v-icon style='font-size:15px'>mdi-bell-check</v-icon>
            </span>
             <template v-if='$device.isDesktop'>
               <span v-if='item.security_type !== "AGG"' style='margin-left:2rem'>
                  {{ formatInstrument(item) }}
               </span>
               <span v-else style='font-weight:600;font-size:15px;'>
                  {{ formatInstrument(item) }}
               </span>
             </template>
             <template v-else>
               <span v-if='item.security_type == "AGG"'>
                  {{ formatInstrument(item, 'simple') }} (Agg) 
               </span>
               <span v-else>
                  {{ formatInstrument(item, 'simple') }}
               </span>
             </template>
          </v-col>
       
          <span v-if='$device.isMobile'>
            <v-col>
              <span :class='`${pnlClass(item)}--text text-right`'>
                <span v-if='marketValue(item)'>
                  {{ toPercent(pnlPct(item)) }} {{ toCurrency(pnl(item)) }} 
                </span>
              </span>
              <br/>
            </v-col>
          </span>
        </v-row>
        <v-row v-if='$device.isMobile'>
          <v-col style='padding:0px'>
            <position-display :editItem='editItem' :position='item'/>
          </v-col>
        </v-row>
      </template>
       <template v-for="field in $store.state.publicGlobals.fields" v-slot:[`item.${field}`]="{ item }">
         <div @contextmenu.prevent="handler" 
           @click='editItem(item, field)' @click.right='editItem(item, field)' style='cursor:pointer'>
    
             <span v-if='item[field]'>
               <template v-if='field == "daily_pnl"'>
                 <span :class='`${pnlClass(item)}--text`'>
                    {{ toCurrency(item[field]) }}
                 </span>
               </template>
               <template v-else>
                 {{ toCurrency(item[field]) }}
               </template>
             </span>
             <span v-else>
               -- 
             </span>
         </div> 
       </template>
       <template v-slot:item.actions="{ item }">
         <v-icon
           small
           class="mr-2"
           @click="editItem(item)"
         >
           mdi-alarm-plus
     
         </v-icon>
       </template>
      </v-data-table>
    </v-flex>
  </v-layout>
</template>

<script>
import AlertDialog from '~/components/AlertDialog.vue';
import PositionDisplay from '~/components/PositionDisplay.vue';
import {sortBy, sumBy} from 'lodash';

export default {
  middleware: ['auth'],
  layout: 'dashboard',
  components: {
    AlertDialog,
    PositionDisplay,
  },
  data(){
    return {
      hasLoadedOnce: false, 
      sortBy: 'instrument',
      sortDesc: false,
    }
  },
  computed: {
    filteredPositions() {
      let positions = [];
      if (this.$device.isDesktop) {
        positions = this.$store.getters.selectedPositions.filter(d => d.security_type !== 'AGG');
      } else {
        positions = sortBy(this.$store.getters.selectedPositions, ["symbol", "security_type"]);
      }
      return positions;
    },
    aggregatePositions() {
      let positions = this.$store.getters.selectedPositions.filter(d => d.security_type == 'AGG');
      return positions;
    },
    headers() {
      let headers = [
         { text: 'Instrument', value: 'instrument'},
      ]
      let desktopHeaders = [
         { text: '#', value: 'position'},
         { text: '', value: 'alert_set'},
         { text: 'Symbol', value: 'symbol', align: ' d-none' },
         { text: 'Price', value: 'price'},
         { text: 'Daily PnL', value: 'daily_pnl'},
         { text: 'Daily PnL %', value: 'pnl_pct_change'},
         { text: 'Value', value: 'value'},
         { text: 'Delta', value: 'delta'},
         { text: 'Gamma', value: 'gamma'},
         { text: 'Vega', value: 'vega'},
         { text: 'Theta', value: 'theta'},
         { text: 'Unrealized PnL', value: 'unrealized_pnl'},
         { text: 'Unrealized PnL %', value: 'unrealized_pct_change'},
         { text: 'Underlying %', value: 'underlying_pct_change'},
         { text: 'Actions', value: 'actions', sortable: false },
      ]
      if (this.$device.isDesktop) {
         headers = headers.concat(desktopHeaders);
      }
      return headers;
    }
  },
  methods: {
    handler(e) {
      e.preventDefault();
    },
    underlyingPrice(items) {
      let position = {};
      let price = null;
      if (items) { 
        items = items.filter(d => d.underlying_price);
        if (items.length > 0){
          price = items[0].underlying_price
 
        }
      }
      return price;
    },
    aggregatePosition(items) {
      let symbol = items ? items[0].symbol : null;
      let position = {};
      if (this.aggregatePositions && symbol) {
        let positions = this.aggregatePositions.filter(d => d.symbol == symbol)
        if (positions) {
          return positions[0];
        }
      }
    },
    editItem(item, field) {
      this.$store.$bus.$emit('editItem', null, item, field)
    },
    makeTableGroupsCollapsed(){
      let table = this.$refs.table;
      let keys = Object.keys(table.$vnode.componentInstance.openCache);
      keys.forEach(x => {
        table.$vnode.componentInstance.openCache[x] = false;
      })
    },
    pnlGroup(positions) {
      return sumBy(positions, d => this.pnl(d));
    },
    pnl(position) {
      return position.daily_pnl;
    },
    updatedDate(position) {
       let updated = this.toUsersTimeZone(position.updated_date)
       updated = this.$moment(updated);
       return updated.fromNow()
    },
    marketValue(position) {
      return position.value
    },
    openingMarketValue(position) {
      let value = 0;
      if (position.position < 0) {
        value = this.marketValue(position) + this.pnl(position);
      } else {
        value = this.marketValue(position) - this.pnl(position);
      }
      return value 
    },
    marketValueGroup(positions) {
      return sumBy(positions, d => this.openingMarketValue(d));
    },
    openPrice(position) {
      return position.price - this.pnl(position);
    },
    pnlPctGroup(positions) {
      return this.pnlGroup(positions)/this.marketValueGroup(positions)
    },
    pnlPct(position) {
      return this.pnl(position)/this.openingMarketValue(position);
    },
    pnlClassGroup(positions) {
      let pnl = this.pnlGroup(positions);
      return pnl >= 0 ? 'green' : 'red';
    },
    pnlClass(position) {
      let pnl = this.pnl(position);
      return pnl >= 0 ? 'green' : 'red';
    },
    pnlArrowGroup(positions) {
      let pnl = this.pnlGroup(positions);
      return pnl >= 0 ? 'mdi-chevron-up' : 'mdi-chevron-down';
    },
    pnlArrow(position) {
      let pnl = this.pnl(position);
      return pnl >= 0 ? 'mdi-chevron-up' : 'mdi-chevron-down';
    }
  },
  watch: {
    "$store.state.positions": function () {
      this.$nextTick(() => {
        if (this.$device.isMobileOrTablet && 
            !this.hasLoadedOnce && 
            this.$store.state.positions.length > 0) {
          this.makeTableGroupsCollapsed();
          this.hasLoadedOnce = true;
        }
      });
    },
  },
  mounted() {
    this.$store.dispatch('getPositions');
    this.$store.dispatch('getAlerts');
  },

}
</script>

<style>
.v-row-group__header {
  background: inherit!important;
}
.v-data-table-header-mobile__wrapper {
  display: none;
}
</style>
