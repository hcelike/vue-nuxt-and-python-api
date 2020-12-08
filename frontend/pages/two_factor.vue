<template>
  <v-layout justify-center align-center style="height: 100%">
    <v-flex xs12 sm8 md4>
      <v-container class="text-center">
        <h1 class="text-center">Two-Factor Authentication</h1>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row>
            <v-col>
              <v-text-field
                v-model="code"
                label="Code"
                outlined
                inputmode="numeric"
                pattern="[0-9]*"
                autocomplete="one-time-code"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col class="d-flex justify-center">
              <v-btn
                :elevation="0"
                :loading='loading'
                color="primary"
                class="rounded-tl-lg rounded-br-lg"
                @click="validate"
              >
                Submit
              </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col class="d-flex justify-center">
              <v-btn
                :elevation="0"
                :loading='loading'
                :text="true"
                @click="sendAgain"
              >
                Send again
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data: () => ({
    valid: true,
    loading: false,
    code: '',
  }),
  methods: {
    sendAgain() {
       this.loading = true;
       this.$axios.$post('/v1/auth/two_factor')
         .then(response => {
            this.$toasted.success("Sent");
         })
         .catch(error => {
            this.$toasted.error(error.response.data.message);
         })
         .finally(()=> {
            this.loading = false;
         })
    },
    validate(){
       this.loading = true;
       this.$axios.$post('/v1/auth/two_factor/validate', {code: this.code})
         .then(response => {
             this.$auth.fetchUser()
               .then(response => {
                  this.$store.dispatch('user/initialRedirect');
               })
         })
         .catch(error => {
            this.$toasted.error("Wrong code");
         })
         .finally(()=> {
            this.loading = false;
         })
    },
  },
  mounted(){
  },
  
}
</script>
