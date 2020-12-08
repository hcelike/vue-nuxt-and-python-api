<template>
  <v-dialog v-model="dialog" max-width="50rem">
    <v-card>
      <v-card-title>
        <span class="headline">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-container>
          <template v-if='livePosition'>
            <template v-if='livePosition.security_type == "STK"'>
              <v-simple-table dense>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left">Price</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td class="text-left"> 
                        {{ toCurrency(livePosition.price) }}
                     </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </template>
            <template v-else-if='["OPT", "AGG"].includes(livePosition.security_type)'>
              <v-simple-table dense>
                <template v-slot:default v-if='!$device.isMobile'>
                  <thead>
                    <tr>
                      <th class="text-left" 
                        v-for='field in $store.state.publicGlobals.fields' 
                        :key='field'>
                        {{ toTitleCase(field) }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td class="text-left"
                        v-for='field in $store.state.publicGlobals.fields' 
                        :key='`${field}-value`'>
                        <span style='cursor:pointer' @click='editedItem.field=field'> 
                          {{ toCurrency(livePosition[field]) }}
                        </span>
                     </td>
                    </tr>
                  </tbody>
                </template>
                <template v-slot:default v-else>
                  <thead>
                    <tr>
                      <th class="text-left" 
                        v-for='field in $store.state.publicGlobals.fields.slice(0, 3)' 
                        :key='field'>
                        {{ toTitleCase(field) }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td class="text-left" 
                        v-for='field in $store.state.publicGlobals.fields.slice(0, 3)' 
                        :key='`${field}-value`'>
                        <span style='cursor:pointer' @click='editedItem.field=field'> 
                          {{ toCurrency(livePosition[field]) }}
                        </span>
                     </td>
                    </tr>
                  </tbody>
             
                  <thead>
                    <tr>
                      <th class="text-left" 
                        v-for='field in $store.state.publicGlobals.fields.slice(3, 7)' 
                        :key='field'>
                        {{ toTitleCase(field) }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td class="text-left" 
                        v-for='field in $store.state.publicGlobals.fields.slice(3, 7)' 
                        :key='`${field}-value`'>
                        <span style='cursor:pointer' @click='editedItem.field=field'> 
                        {{ toCurrency(livePosition[field]) }}
                        </span>
                     </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </template>
          </template>
          <v-form v-model="valid" ref="form">
            <v-row :dense='dense' no-gutter>
              <v-col cols="12" sm="6" md="6">
                <v-select
                  :items="positions"
                  v-model="editedItem.position"
                  label="Position"
                  :item-text="item =>`${formatInstrument(item)}`"
                  item-value='id'
                  return-object
                  :dense="dense"
                  filled
                >
                </v-select>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-select
                  :items="$store.state.publicGlobals.fields"
                  v-model="editedItem.field"
                  required
                  :rules='rules'
                  label="Field"
                  :dense="dense"
                  filled
                >
                </v-select>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-select
                  :items="$store.state.publicGlobals.conditions"
                  v-model="editedItem.condition"
                  label="Condition"
                  filled
                  :rules='rules'
                  :dense="dense"
                  required
                >
                </v-select>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-row no-gutter>
                  <v-col cols='11'>
                    <span style='display:inline'>
                      <v-text-field 
                        v-model="editedItem.value" 
                        :rules='rules'
                        required 
                        :dense="dense"
                        label="Value">
                      </v-text-field>
                      <v-icon small @click='setValue'>mdi-refresh</v-icon>
                    </span>
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-select
                  :items="['email', 'sms']"
                  v-model="editedItem.alert_types"
                  label="Alert Types"
                  multiple
                  :dense="dense"
                  :rules="[v => v.length > 0 || 'Item is required']"
                  :required='true'
                >
                </v-select>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-menu
                  ref="menu"
                  v-model="menu"
                  :close-on-content-click="false"
                  :return-value.sync="editedItem.expiration_date"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="editedItem.expiration_date"
                      label="Expiration"
                      readonly
                     :dense="dense"
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="editedItem.expiration_date" no-title scrollable>
                    <v-spacer></v-spacer>
                    <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
                    <v-btn text color="primary" @click="$refs.menu.save(editedItem.expiration_date)">OK</v-btn>
                  </v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="12" sm="12" md="12">
                <v-text-field 
                  v-model="editedItem.message" 
                  :dense="dense"
                  label="message">
                </v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
        <v-btn color="blue darken-1" :disabled="!valid" text @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>

export default {
  props: {
    positions: {
      required: true,
      type: Array,
    },
    
  },  
  data(){
    return {
      dialog: false,
      dense: this.$device.isMobile,
      valid: false,
      editedIndex: -1,
      rules: [
        v => !!v || 'Item is required',
      ],
      menu: false,
      editedItem: {
        position: null, 
        condition: 'greater than',
        value: 0,
        field: 'price',
        expiration_date: null,
        alert_types: ['sms'],
        message: '',
      },
      defaultItem: {
        position: null, 
        condition: 'greater than',
        value: 0,
        field: 'price',
        expiration_date: null,
        alert_types: ['sms'],
        message: '',
      },
    }
  },
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Alert' : 'Edit Alert'
    },
    livePosition() {
      let position = null;
      if (this.editedItem.position) {
        let positions = this.$store.state.positions;
        let id = this.editedItem.position.id;
        for (let pos of positions) {
          if (pos.id == id) {
            position = pos;
            break;
          }
        }
      }
      return position;
    },
  },
  watch: {
    dialog (val) {
      val || this.close()
    },
    editedItem: {
      deep: true,
      handler(){
        this.setMessage();
      }
    },
    "editedItem.field": function () {
       this.setValue();
    },
  },
  methods: {
    editItem (alert, position, field) {
      this.editedIndex = this.$store.state.alerts.indexOf(alert)
       
      if (alert) {
        let newItem = Object.assign({}, alert);
        if (alert.expiration_date){
          let expiration_date = this.makeCopy(alert.expiration_date).split('T')[0];
          newItem.expiration_date = expiration_date;
        }
        this.editedItem = newItem;
      } 
      else {
        let newItem = Object.assign({}, this.defaultItem);
        if (position.expiration_date) {
          let expiration_date = this.makeCopy(position.expiration_date).split('T')[0];
          newItem.expiration_date = expiration_date;
        }
        field = field ? field : this.makeCopy(this.editedItem.field);
        let value = position[field];
        this.editedItem = Object.assign(newItem, {
          position: position, 
          field: field, 
          value: value, 
        })
        this.setMessage()
      }
      this.dialog = true
    },
    setMessage(){
      if (this.editedItem.position) {
        let message = `${this.formatInstrument(this.editedItem.position)} `;
        message += `${this.editedItem.field} is ${this.editedItem.condition} ${this.editedItem.value}`; 
        this.editedItem.message = message; 
      } 
    },
    setValue(){
      if (this.editedItem.position) {
        this.editedItem.value = this.livePosition[this.editedItem.field];
      } 
    },
    close () {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
    save () {
       if (this.$refs.form.validate()){
         if (this.editedIndex > -1) {
           this.$store.dispatch('editAlert', this.editedItem);
         } else {
           this.$store.dispatch('addAlert', this.editedItem);
         }
         this.close()
       } 
    },
  },
  mounted() {
    this.$store.$bus.$on('editItem', this.editItem)
  },  

}
</script>
