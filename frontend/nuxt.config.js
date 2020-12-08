import colors from 'vuetify/es5/util/colors'

export default {
  // 'universal' mode breaks secure sessions since 
  // requests from serverside rendering don't include
  // session httponly cookies
  // whereas 'spa' has all requests from browser 
  mode: 'spa',
  /*
   ** Headers of the page
   */
  server: {
    host: '127.0.0.1',
    port: 8081
  },
  publicRuntimeConfig: {},
  privateRuntimeConfig: {
  },
  head: {
    titleTemplate: '%s - ' + process.env.BRAND_NAME,
    title: process.env.BRAND_NAME || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || ''
      }
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },
  /*
   ** Customize the progress-bar color
   */
  loading: { color: '#fff' },
  /*
   ** Global CSS
   */
  css: [],
  /*
   ** Plugins to load before mounting the App
   */
  plugins: [
    '~plugins/global_event_bus.js', 
    { src: '~/plugins/nuxt_client_init.js', ssr: false }, 
    '~/plugins/utils.js', 
    '~/plugins/global_mixins.js'
  ],
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: [
    '@nuxtjs/vuetify',
    '@nuxtjs/moment',
  ],
  moment: {
    timezone: true
  },
  /*
   ** Nuxt.js modules
   */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/auth',
    '@nuxtjs/toast',
    '@nuxtjs/pwa',
    'nuxt-socket-io',
    '@nuxtjs/device',
  ],
  /*
   ** Axios module configuration
   ** See https://axios.nuxtjs.org/options
   */
  axios: {
    baseURL: process.env.API_ENDPOINT,
    credentials: true,
    headers: {
      common: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
        Accept: 'application/json'
      }
    }
  },
  toast: {
    position: 'top-center',
    duration: 5000,
    theme: 'outline',
  },
  io: {
    // module options
    sockets: [{
      name: 'main',
      url: process.env.API_ENDPOINT,
    }]
  },
  auth: {
    redirect: {
        login: '/login',
        logout: '/login',
        callback: '/login',
        home: '/login'
    },
    plugins: [ '~/plugins/auth.js' ],
    strategies: {
      local: {

        endpoints: {
          login: {
            url: '/v1/auth',
            method: 'post',
            propertyName: 'access_token',
          },
          logout: { url: '/v1/auth', method: 'delete'},
          user: { url: '/v1/user', method: 'get', propertyName: false}
        },
        tokenRequired: true,
        tokenType: 'Bearer',
        globalToken: true,
        autoFetchUser: false,
      }
    }
  },
  /*
   ** vuetify module configuration
   ** https://github.com/nuxt-community/vuetify-module
   */
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    icons: {
      iconfont: 'mdi' // default - only for display purposes
    },
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        },
        light: {
          primary: {
            light: 'black',
            contrastText: 'white'
          }
        }
      }
    }
  },
  /*
   ** Build configuration
   */
  build: {
    /*
     ** You can extend webpack config here
     */
    extend(config, ctx) {}
  }
}
