<template>
  <v-layout justify-center align-center style="height: 100%">
    <v-flex xs12 sm8 md4>
      <v-container class="text-center">
        <h1 class="text-center">Create an account</h1>
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
                v-model="phone_number"
                :rules="phone_number_rules"
                label="Phone Number"
                hint='10 digits'
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
                hint='6 characters or more'
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
                @click="signup"
              >
                Sign Up
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
        <div style="margin-top: 1rem">
           <nuxt-link to='/login'>Already have an account?</nuxt-link>
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
    email: null,
    phone_number_rules: [v => !!v || 'Phone Number is required'],
    phone_number: null,
    emailRules: [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
    ],
    passwordRules: [v => !!v || 'Password is required'],
    password: null
  }),
  methods: {
    async signup() {
      this.loading = true
      this.$axios
        .$post('/v1/user', {
          email: this.email,
          password: this.password,
          phone_number: this.phone_number,
        })
        .then(response => {
          let data = {
            email: this.email,
            password: this.password
          }
          this.$store.dispatch('user/login', data)
        })
        .catch(error => {
          this.$toast.error(error.response.data.message);
        })
        .finally(() => {
          this.loading = false
        })
    },
  },
  mounted(){
  },
  
}
</script>
