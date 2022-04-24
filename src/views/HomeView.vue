<template>
    <div class="container-fluid">
      <div class="d-flex banner">
        <div class="container col-6 flex-column">
          <h1>{{ message }}</h1>
          <p> United Auto Sales provides the fastest, easiest and most
              user-friendly way to buy or sell cars online. Find a Great Price 
              on the Vehicle You Want.
          </p>

          <div class="d-flex row">
            <button @click="register" class="btn btn-primary col-5 mx-2">Register</button>
            <button @click="login" class="btn btn-success col-5 mx-2">Login</button>
          </div>
        </div>
        <img alt="Car photo" class="col-6" src="@/assets/banner.jpg" />
      </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            message: "Buy and Sell Cars  Online"
        };
    },
    methods: {
      register() {
        let self = this;
        // redirect to register page
        self.$router.push({ path: '/register'});
      },
      login() {
        let self = this;
        // redirect to login page
        self.$router.push({ path: '/login'});
      }
    }
}
</script>

<style scoped>
.banner {
  width:100%;
  height: auto;
}
.banner .container {
  width: 25%;
  justify-content: center;
}
img {
  object-fit: cover;
}
</style>