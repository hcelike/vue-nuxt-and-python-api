import {map} from 'lodash';

export const state = () => ({
})

export const mutations = {
}

export const actions = {
  logout({dispatch, state, commit, rootState}){
     this.$auth.logout();
  }, 
  login({dispatch, state, commit, rootState}, data){
     return new Promise((resolve, reject) => {
       this.$auth.loginWith('local', {data})
         .then(response => {
            if (response.data.requires_two_factor){
               this.$router.push({path: '/two_factor'});
            } else {
               this.$auth.fetchUser()
                 .then(response => {
                    dispatch('initialRedirect');
                    resolve()
                 })
             }
         })
         .catch(error => {
            console.log(error);
            reject(error);
         })
     })
  },
  initialRedirect({dispatch, state, commit, getters}){
     let path = '/';
     if (this.$auth.user.role == "admin") {
       path = '/admin/dashboard';
     }
     this.$router.replace({
       path: path,
     })
  },
}

