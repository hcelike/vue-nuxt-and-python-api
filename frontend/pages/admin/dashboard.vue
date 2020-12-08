<template>
  <v-flex style="margin: 0; min-height: 100vh;" class="d-flex" :elevation="0">
    <v-container>
     <h1>Users</h1>
  <v-spacer></v-spacer>
 <br/>

      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        style='max-width:500px'
        outlined
        dense
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
 <br/>
      <template>
        <v-data-table
          :headers="headers"
          :search="search"
          :items="users"
          :items-per-page="100"
          class="elevation-1"
        >
         <template v-slot:item.login="{ item }">
           <v-btn color='primary' x-small @click='login(item.id)'>Login as</v-btn>
         </template>
        </v-data-table>
      </template>
    </v-container>
  </v-flex>
</template>

<script>
import {map} from 'lodash';
export default {
  middleware: ['auth'],
  meta: {
    role: 'admin',
  },
  data: () => ({
    users: [],
    search: null,
    headers: [
       { text: 'Login', value: 'login' },
       { text: 'Id', value: 'id' },
       { text: 'Email', value: 'email' },
       { text: 'First Name', value: 'first_name' },
       { text: 'Last Name', value: 'last_name' },
    ],
  }),
  methods: {
    getUsers(){
      this.$axios.get('/v1/admin/users')
        .then(response => {
          this.users = response.data.data;
        })
     },
     login(id) {
       this.$axios.post('/v1/admin/users', {id})
       .then(response =>{ 
            this.$auth.setUserToken(response.data.access_token)
               .then(() => {
                 this.$auth.fetchUser()
                    .then(response => {
                       this.$store.dispatch('user/initialRedirect');
                    })
               })
       })
       .catch((error)=> { 
           this.$toasted.error(error.response.data.message);
       })
   
     },
  },
  mounted() {
    this.getUsers();
  },
}
</script>
<style lang="scss">
</style>
