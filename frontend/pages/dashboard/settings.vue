<template>
  <v-container>
    <h1>Settings</h1>
    <v-flex class="flex-nowrap">
      <v-card max-width="80%">
        <v-card-text>
          <h4 class="special" style=""></h4>
          <v-form
            ref="form"
            v-model="valid_basic_info"
            lazy-validation
            class="account-form"
          >
            <v-row>
              <v-col>
                <v-text-field
                  v-model="phone_number"
                  :rules="phone_number_rules"
                  label="Phone Number"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
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
              <v-col>
                <v-switch
                  v-model="enable_sound_alerts"
                  :label="enable_sound_alerts ? 'Enable Sound Alerts' : 'Disable Sound Alerts'"
                ></v-switch>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-switch
                  v-model="enable_voice_alerts"
                  :label="enable_voice_alerts ? 'Enable Voice Alerts' : 'Disable Voice Alerts'"
                ></v-switch>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-switch
                  v-model="requires_two_factor"
                  color='orange'
                  :label="requires_two_factor ? 'Two-Factor Auth Enabled' : 'Two-Factor Auth Disabled'"
                ></v-switch>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="d-flex">
                <v-btn
                  :elevation="0"
                  :loading="loading"
                  color="primary"
                  class="rounded-tl-lg rounded-br-lg"
                  @click="save_basic_info"
                >
                  Save
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
      </v-card>
      <br />
      <v-card max-width="80%">
        <v-card-text>
          <h4 class="special">Connect Interactive Brokers Account</h4>
          <br/>
          <template v-if='$store.getters.isBrokerageConnected'>
            <v-alert dense type="success" >
              Connected to {{ $store.state.brokerage_connection.ib_username  }}
            </v-alert>
            <v-btn @click='$store.dispatch("disconnectBrokerage")'>Disconnect Brokerage</v-btn>
          <br/>
          </template>
          <template v-else>
            <v-alert dense  type="warning">
              Not Connected 
            </v-alert>
            <v-btn @click='$store.$bus.$emit("openConnectBrokerage")'>Connect Brokerage</v-btn>
          <br/>
          </template>
          <br/>
        </v-card-text>
      </v-card>
      <br />
      <v-card max-width="80%">
        <v-card-text>
          <h4 class="special">Change Password</h4>
          <v-form
            v-model="valid_change_password"
            lazy-validation
            class="account-form"
          >
            <v-row>
              <v-col>
                <v-text-field
                  v-model="current_password"
                  :rules="current_password_rules"
                  label="Current Password"
                  type="password"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="new_password"
                  :rules="new_password_rules"
                  label="New Password"
                  type="password"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="confirm_new_password"
                  :rules="[
                    validate_password_confirmation,
                    confirm_new_password_required
                  ]"
                  type="password"
                  label="Confirm New Password"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="d-flex">
                <v-btn
                  :elevation="0"
                  :loading="loading"
                  color="primary"
                  class="rounded-tl-lg rounded-br-lg"
                  @click="submit_new_password_info"
                >
                  Save
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-container>
</template>

<script>
import { getUrlParameter } from '@/utils/utils.js'
export default {
  layout: 'dashboard', 
  components: {
  },
  data: () => ({
    valid_basic_info: true,
    valid_change_password: true,
    loading: false,
    current_password: '',
    new_password: '',
    confirm_new_password: '',
    enable_sound_alerts: null,
    enable_voice_alerts: null,
    requires_two_factor: false,
    phone_number_rules: [v => !!v || 'Phone Number is required'],
    phone_number: '',
    email: '',
    emailRules: [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
    ],
    current_password_rules: [v => !!v || 'Current Password is required'],
    new_password_rules: [v => !!v || 'New Password is required']
  }),
  methods: {
    setData(){
      this.email = this.$store.state.auth.user.email
      this.phone_number = this.$store.state.auth.user.phone_number
      this.enable_voice_alerts = this.$store.state.auth.user.enable_voice_alerts
      this.enable_sound_alerts = this.$store.state.auth.user.enable_sound_alerts
      this.requires_two_factor = this.$store.state.auth.user.requires_two_factor
    },
    async save_basic_info() {
      let data = {
        email: this.email,
        phone_number: this.phone_number,
        enable_voice_alerts: this.enable_voice_alerts,
        enable_sound_alerts: this.enable_sound_alerts,
        requires_two_factor: this.requires_two_factor,
      }
      this.loading = true
      this.$axios.put('/v1/user', data)
        .then(response => {
          this.$toasted.success('Saved');
          this.$auth.fetchUser().then(()=> this.setData());
        })
        .catch(error => {
          this.$toasted.error(error.response.data.message);
        })
        .finally(() => {
          this.loading = false
        })
    },
    async submit_new_password_info() {
      let data = {
        current_password: this.current_password,
        password: this.new_password,
        password_confirm: this.confirm_new_password
      }
      this.loading = true
      this.$axios.put('/v1/auth/change', data)
        .then(response => {
          this.$toasted.success('Changed');
        })
        .catch(error => {
          this.$toasted.error(error.response.data.message);
        })
        .finally(() => {
          this.loading = false
        })

    },
    validate_password_confirmation(v) {
      let new_password = this.new_password
      return (
        v == new_password || 'Confirmed password is different from New Password'
      )
    },
    confirm_new_password_required(v) {
      return !!v || 'Confirm New Password is required'
    }
  },
  mounted() {
    this.setData()
  },
}
</script>
<style lang="scss">
.account-form {
  width: 100%;
}
</style>
