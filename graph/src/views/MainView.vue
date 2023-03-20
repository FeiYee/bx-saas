<template>
  <Header />
  <div>
    <RouterView />
  </div>
  <Footer />
</template>
<script setup>
import { RouterView } from 'vue-router'
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'
</script>
