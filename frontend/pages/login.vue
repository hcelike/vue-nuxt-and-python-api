<template>
  <v-layout justify-center align-center style="height: 100%">
    <v-flex xs12 sm8 md4>
      <v-container class="text-center">
        <h1 class="text-center">Login</h1>
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
            <v-col>
              <v-text-field
                v-model="password"
                :rules="passwordRules"
                label="Password"
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
                @click="login"
              >
                Login
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
        <div style="margin-top: 1rem">
           <nuxt-link to='/forgot_password'>Forgot Password?</nuxt-link>
           <br/>
           <nuxt-link to='/signup'>Need an account? Signup</nuxt-link>
        </div>
      </v-container>
    </v-flex>
  </v-layout>
</template>

<script>
import {getUrlParameter} from '@/utils/utils.js';

export default {
  data: () => ({
    valid: true,
    loading: false,
    email: '',
    emailRules: [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
    ],
    passwordRules: [v => !!v || 'Password is required'],
    password: ''
  }),
  methods: {
    async login() {
       let data = {
           email: this.email,
           password: this.password
       }
       this.loading = true;
       this.$store.dispatch('user/login', data)
         .catch(error =>{
           this.$toasted.error('Wrong email/password combination');
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
