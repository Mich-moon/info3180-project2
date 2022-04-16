<template>
    <div class="home">
      <div class="d-flex banner">
        <div class="container col-6 d-flex flex-column">
          <h1>{{ message }}</h1>
          <p> United Auto Sales provides the fastest, easiest and most
              user-friendly way to buy or sell cars online. Find a Great Price 
              on the Vehicle You Want.
          </p>

          <div class="d-flex row">
            <button class="btn btn-primary col-5 mx-2">Register</button>
            <button class="btn btn-primary col-5 mx-2">Login</button>
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
}
</script>

<style>
.banner {
  width:100%;
  height: auto;
}
.banner .container {
  width: 25%;
  justify-content: center;
}
.home {
  width: 100%;
}
img {
  object-fit: cover;
}
</style>