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
              <RouterLink class="nav-link" to="/cars/new">Add Car</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/users/ + id">My Profile</RouterLink>
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
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
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
        logged_in: false, 
        profile_route: ""
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

          // retrieve user id from token stored in localstorage
          let jwt_token = localStorage.getItem("token");

          var base64Url = jwt_token.split('.')[1];
          var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
          var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
          }).join(''));

          let jwt_payload = JSON.parse(jsonPayload);
          let id = jwt_payload['sub'];
          console.log(id);

          self.profile_route = "/users/" +  id;

        } else {
          self.logged_in = false;
        }
      },
      logout() {
        let self = this;
        self.logged_in = false;
        localStorage.removeItem("token");
        // redirect to home page
        self.$router.push({ path: '/'});
      }
    },
  };
</script>

<style>
nav {
  background-color: rgb(13, 54, 70);
}
</style>