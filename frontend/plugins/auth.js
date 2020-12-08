import {map} from 'lodash';

export default function ({ $auth , route, redirect}) {
  if (route.meta && route.meta[0]){
    const roleRequired = route.meta[0].role;
    if (!$auth.user){
       return 
    }
    if (roleRequired){
      const roles = map($auth.user.roles, 'name')
      if (!roles.includes(roleRequired)){
        return redirect('/404');
      }
    } else {
      return 
    }
  }
}
