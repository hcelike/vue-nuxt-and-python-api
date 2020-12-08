<template>
  <v-layout column justify-center align-center style="height: 100%">
    <v-flex xs12 sm8 md6>
      <v-container class="text-center">
        <h1 class="text-center">Confirm Your Email</h1>
        <p class="text-center">We've sent you an email with a confirmation link.</p>
 
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row>
            <v-col>
              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="Work email"
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
                @click="resend"
              >
                Resend
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
    </v-flex>
  </v-layout>
</template>

<script>
import {getUrlParameter} from '@/utils/utils.js';

export default {
  data: () => ({
    loading: false,
    valid: false,
    form: {
       token: null,
    },
    email: '',
    emailRules: [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
    ],
  }),
  methods: {
    async submitConfirm() {
       this.loading = true;
       this.$axios.$post('/v1/auth/confirm/email', this.form)
           .then(response =>{
              this.loading = false;
              this.$toasted.success('Confirmed');
              this.$auth.fetchUser()
                 .then(() => {
                     this.$store.dispatch("user/initialRedirect");
                 })
           })
           .catch(error => {
              this.$toasted.error(error.response.data.message);
           })
           .finally(()=> {
              this.loading = false;
           })
      },
    resend() {
       this.loading = true;
       this.$axios.$put('/v1/auth/confirm/email', {email: this.email})
           .then(response =>{
              this.loading = false;
              this.$toasted.success('Email sent');
           })
           .catch(error => {
              this.$toasted.error(error.response.data.message);
           })
           .finally(()=> {
              this.loading = false;
           })
      },
  },
  mounted(){
     this.form.token = getUrlParameter("token");
    
     this.email = this.$auth.user.email;
     if (this.form.token){
         this.submitConfirm();
     }
     if (this.$auth.user.confirmed_emails.includes(this.$auth.user.email)){
         this.$store.dispatch('user/initialRedirect');
     }
  },
  
}
</script>
