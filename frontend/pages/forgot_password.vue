<template>
  <v-layout justify-center align-center style="height: 100%">
    <v-flex xs12 sm8 md4>
      <v-container class="text-center">
        <h1 class="text-center">Forgot Password</h1>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row>
            <v-col>
              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="Email"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col class="d-flex justify-center">
              <v-btn
                :elevation="0"
                :loading='loading'
                @click="submitReset"
              >
                Send reset link
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
        <div style="margin-top: 1rem">
          Remember your password? <nuxt-link to="/login">Login</nuxt-link>
        </div>
      </v-container>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data: () => ({
    valid: true,
    loading: false,
    email: '',
    emailRules: [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
    ],
  }),
  methods: {
    async submitReset() {
       let data = {
           email: this.email,
       }
       this.loading = true;
       this.$axios.$post('/v1/auth/reset', data)
         .then(response => {
            this.$toasted.success('If your email exists, a link is on its way')
         })
         .catch(error => {
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
