<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
      <div class="container-fluid">
        <span class="mx-2"/>
        <a class="navbar-brand" href="/"><span class="iconify-inline mx-2" data-icon="ion:car"/> United Auto Sales</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto" v-if="(logged_in == true)">
            <li class="nav-item">
              <span class="mx-4"/><span class="mx-4"/>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/about">Add Car</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/about">Explore</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/about">My Profile</RouterLink>
            </li>
          </ul>
          <ul class="navbar-nav me-auto" v-else>
            <li class="nav-item">
              <span class="mx-4"/><span class="mx-4"/>
            </li>
          </ul>

          <ul class="navbar-nav mx-4" v-if="logged_in">
            <li class="nav-item">
              <a @click="logout" class="nav-link" href="#">Logout</a>
            </li>
          </ul>
          <ul class="navbar-nav mx-4" v-else>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/about">Register</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/about">Login</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
import { RouterLink } from "vue-router";

  export default {
    data() {
      return {
        logged_in: false
      }
    },
    created() {
      this.isLoggedIn();
    },
    methods: {
      isLoggedIn() {
        let self = this;

        if (localStorage.getItem("token")) {
          self.logged_in = true;
        } else {
          self.logged_in = false;
        }
      },
      logout() {
        let self = this;
        self.logged_in = false;
      }
    },
  };
</script>

<style>
nav {
  background-color: rgb(13, 54, 70);
}
</style>