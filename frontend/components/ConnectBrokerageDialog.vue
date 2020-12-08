<template>
  <v-dialog v-model="dialog" max-width="25rem">
    <v-card>
      <v-card-title class='display:block'>
        <p class="text-center">{{ formTitle }}</p>
      </v-card-title>
      <v-card-text>
        <p class="text-center">Interactive Brokers Account</p>
        <p>Tip: To connect Interactive Brokers here without cutting off your other sessions or in order to limit permissions, create a separate username specifically for API access. (More info: <a href='https://ibkr.info/node/1004' target='_blank'>https://ibkr.info/node/1004</a>).</p>
        <v-container>
          <v-form v-model="valid" ref="form">
            <v-row no-gutter>
              <v-col cols="12" sm="12" md="12">
                <v-select
                  :items="['paper', 'live']"
                  v-model="form.trading_mode"
                  label="Trading Mode"
                  :rules="rules"
                  filled
                  :required='true'
                >
                </v-select>
              </v-col>
              <v-col cols="12" sm="12" md="12">
                <v-text-field 
                  v-model="form.username"
                  :rules='rules'
                  required 
                  label="Username">
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="12" md="12">
                <v-text-field 
                  v-model="form.password"
                  :rules='rules'
                  required 
                  :append-icon="value ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append="() => (value = !value)"
                  :type="value ? 'password' : 'text'"
                  label="Password">
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
  },  
  data(){
    return {
      dialog: false,
      valid: false,
      value: true,
      rules: [
        v => !!v || 'Item is required',
      ],
      form: {
        trading_mode: 'paper',
        username: null,
        password: null,
      },
    }
  },
  computed: {
    formTitle () {
      return 'Connect'
    },
  },
  watch: {
    dialog (val) {
      this.value = true;
      val || this.close()
    },
  },
  methods: {
    close () {
      this.dialog = false
    },
    open () {
      this.dialog = true
    },
    save () {
      this.$store.dispatch('connectBrokerage', this.form)
        .then(response => {
          this.$store.commit('showSnackBar', "Connecting to IB");
          this.close()
        })
        .catch(error => {
        })
    },
  },
  mounted() {
    this.$store.$bus.$on('openConnectBrokerage', this.open)
  },  

}
</script>

<style>
.v-card__title {
  display: block;
}
</style>
