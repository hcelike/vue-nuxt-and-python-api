<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
    >
      <v-list dense>
        <template v-if='$auth.user.role !== "admin"'>
          <v-list-item>
            <select-brokerage-account-id style='max-width:200px;margin-top:30px;margin-right:20px;'/>
          </v-list-item>
          <v-list-item to="/dashboard/risk" link>
            <v-list-item-action>
              <v-icon>mdi-view-dashboard</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Risk Dashboard</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/dashboard/alerts" link>
            <v-list-item-action>
              <v-icon>mdi-alarm-plus</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Alerts</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/dashboard/alert_events" link>
            <v-list-item-action>
              <v-icon>mdi-alarm-check</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Alert Events</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
        <template v-else>
          <v-list-item to="/admin/dashboard" link>
            <v-list-item-action>
              <v-icon>mdi-account-multiple</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Users</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
      
        </template>
        <v-list-item to='/dashboard/settings' link>
          <v-list-item-action>
            <v-icon>mdi-cog</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Settings</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click='$store.dispatch("user/logout")'>
          <v-list-item-action>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Log Out</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      clipped-left
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title> {{ $store.state.publicGlobals.brand_name }}</v-toolbar-title>

      <v-spacer></v-spacer>
      <template v-if='$auth.user.role !== "admin"'> 
        <template v-if='$store.getters.isBrokerageConnected'>
          <v-toolbar-title>
          <v-alert class='alert-top' outlined dense type="success" >
             Connected to {{ $store.state.brokerage_connection.ib_username  }}
          </v-alert>
          </v-toolbar-title>
        </template>
        <template v-else>
            <v-toolbar-title>
            <template v-if='$store.state.brokerage_connection.status == "CONNECTING"'>
              <v-alert class='alert-top' outlined dense type="warning" >
                <span style='cursor:pointer' @click='$store.$bus.$emit("openConnectBrokerage")'>
                  Connecting to {{ $store.state.brokerage_connection.ib_username }}
                </span>
              </v-alert>
            </template>
            <template v-else>
              <v-alert class='alert-top' outlined dense type="error" >
                <span style='cursor:pointer' @click='$store.$bus.$emit("openConnectBrokerage")'>
                  Disconnected from IB
                </span>
              </v-alert>
            </template>
            </v-toolbar-title>
        </template>
      </template>
    </v-app-bar>

    <v-main>
      <v-container
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col>
            <nuxt />

          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <v-snackbar v-model="$store.state.snackbar" :timeout='$store.state.snackbar_timeout'>
      {{ $store.state.snackbar_text }}
      <template v-slot:action="{ attrs }">
        <v-btn
          color="pink"
          text
          v-bind="attrs"
          @click="$store.commit('removeSnackBar')"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
    <connect-brokerage-dialog/>


    <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }} {{ $store.state.publicGlobals.company_name }}</span>
    </v-footer>
  </v-app>
</template>

<script>
  import SelectBrokerageAccountId from '~/components/SelectBrokerageAccountId';
  import ConnectBrokerageDialog from '~/components/ConnectBrokerageDialog';

  export default {
    components: {
      SelectBrokerageAccountId,
      ConnectBrokerageDialog,
    },
    props: {
      source: String,
    },
    data: () => ({
      drawer: null,
    }),
    created () {
      this.$vuetify.theme.dark = true
    },
  }
</script>

<style>
.alert-top {
  margin-bottom: 0px!important;
  padding: 2px !important;
  padding-right: 5px !important;
  font-size: 10px !important;
}
.v-application--is-ltr .v-alert__icon {
  margin-right: 0px !important; 
  font-size: 13px !important;
}
</style>
