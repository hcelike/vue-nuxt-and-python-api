<template>
  <nuxt-child/>
</template>

<script>
export default {
  layout: 'dashboard',
  middleware: ['auth'],
  mounted() {
 
  },
}
</script>
