<template> 
  <v-simple-table dense>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left" 
            v-for='field in fields.slice(0, 4)' 
            :key='field'>
            {{ toTitleCase(field) }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="text-left" 
            v-for='field in fields.slice(0, 4)'
            :key='`${field}-value`'>
            <span style='cursor:pointer' @click='editItem(position, field)' @click.right='editItem(position, field)'>
            {{ toCurrency(position[field]) }}
            </span>
         </td>
        </tr>
      </tbody>
      <thead>
        <tr>
          <th class="text-left" 
            v-for='field in fields.slice(4, fields.length)' 
            :key='field'>
            {{ toTitleCase(field) }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="text-left" 
            v-for='field in fields.slice(4, fields.length)'
            :key='`${field}-value`'>
            <span style='cursor:pointer' @click='editItem(position, field)' @click.right='editItem(position, field)'>
              {{ toCurrency(position[field]) }}
            </span>
         </td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template> 

<script>
export default {
  props: {
    position: {
      required: true,
      type: Object,
    },
    editItem: {
      required: true,
      type: Function,
    },
  },
  computed: {
    fields() {
      let fields = ['price', 'daily_pnl', 'pnl_pct_change', 'unrealized_pct_change'];
      if (["AGG", "OPT"].includes(this.position.security_type)){
        fields = fields.concat(['delta', 'gamma', 'theta', 'vega']) 
      } 
      return fields;
    },
  },
  data() {
    return {
    }
  },
}
</script>

<style>
.v-data-table--dense > .v-data-table__wrapper > table > tbody > tr > th, .v-data-table--dense > .v-data-table__wrapper > table > thead > tr > th, .v-data-table--dense > .v-data-table__wrapper > table > tfoot > tr > th {
    height: 10px;
}
</style>
