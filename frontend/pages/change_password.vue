<template>
  <v-layout justify-center align-center style="height: 100%">
    <v-flex xs12 sm8 md4>
      <v-container class="text-center">
        <div v-if='invite'>
          <h1 class="text-center">Welcome to {{$store.state.publicGlobals.brand_name}}</h1>
          <h4 class="text-center">Please set your password</h4>
        </div>
        <div v-else>
          <h1 class="text-center">Change Your Password</h1>
        </div>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row>
            <v-col>
              <v-text-field
                v-model="form.password"
                :rules="passwordRules"
                label="Password"
                type="password"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                v-model="form.password_confirm"
                :rules="passwordRules"
                label="Re-type Password"
                type="password"
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
                @click="reset"
              >
                Change Password
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
    </v-flex>
  </v-layout>
</template>

<script>
import {getUrlParameter} from '~/utils/utils.js';

export default {
  data: () => ({
    valid: true,
    loading: false,
    passwordRules: [v => !!v || 'Password is required'],
    invite: null,
    form: {
       password: '',
       token: null,
       password_confirm: ''
    },
  }),
  methods: {
    async reset() {
       this.loading = true;
       this.$axios.$put('/v1/auth', this.form)
           .then(response =>{
              this.$toasted.success('Password Changed');
              this.loading = true;
              let data = {email: response.email, password: this.form.password}
              this.$store.dispatch('user/login', data)
                .catch(error =>{
                  this.$toasted.error('Wrong email/password combination');
                 })
                .finally(()=> {
                   this.loading = false;
                })
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
     this.invite = getUrlParameter("invite");
  },
  
}
</script>
