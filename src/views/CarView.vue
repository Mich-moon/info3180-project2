<template>
  <div class="container-fluid d-flex flex-column">
    <div id="messages" :class="msgClass" :v-if="msgClass">
      <ul class="msg__list">
        <li v-for="(message, index) in messages" :key="index" class="msg__item">
          {{ message }}
        </li>
      </ul>
    </div>

    <div class="row px-0 component mb-5 px-2">
      <div class="col-5 mx-0 p-2">
        <img class="card-img-top" :src="'/uploads/' + car.photo" />
      </div>
      <div class="col-7 mx-0 p-2">
        <div>
          <h3>{{ car.year }} {{ car.make }}</h3>
          <h5>{{ car.model }}</h5>
          <p class="py-4">{{ car.description }}</p>
          <p class="row">
            <span class="col-6"
              ><span>Colour: </span
              ><span class="fw-bold"> {{ car.colour }}</span></span
            >
            <span class="col-6"
              ><span>Body Type: </span
              ><span class="fw-bold"> {{ car.car_type }}</span></span
            >
            <span class="col-6"
              ><span>Price: </span
              ><span class="fw-bold"> {{ car.price }}</span></span
            >
            <span class="col-6"
              ><span>Transmission: </span
              ><span class="fw-bold"> {{ car.transmission }}</span></span
            >
          </p>
          <div class="row">
            <button
              @click.prevent="email"
              type="button"
              id="email-btn"
              class="col-6 btn btn-success"
            >
              Email Owner
            </button>
            <div class="col-6 like">
              <button
                @click.prevent="like"
                type="button"
                id="like-btn"
                class="btn btn-outline-danger btn-circle"
              >
                <span
                  class="iconify-inline"
                  data-icon="ant-design:heart-outlined"
                ></span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: [ 'car_id' ],
  data() {
    return {
      csrf_token: "",
      user_id: null,
      messages: [],
      msgClass: "",
      car: {}
    };
  },
  created() {
    this.isLoggedIn();
    this.getCsrfToken();
    this.getCar();
  },
  methods: {
    isLoggedIn() {
      let self = this;

      if (localStorage.getItem("token")) {
        self.logged_in = true;

        // retrieve user id from token stored in localstorage
        let jwt_token = JSON.parse(localStorage.getItem("token"));

        var base64Url = jwt_token.split(".")[1];
        var base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
        var jsonPayload = decodeURIComponent(
          atob(base64)
            .split("")
            .map(function (c) {
              return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
            })
            .join("")
        );

        let jwt_payload = JSON.parse(jsonPayload);
        self.user_id = jwt_payload["sub"];
      } else {
        // redirect to home page
        self.$router.push({ path: "/" });
      }
    },
    getCar() {
      let self = this;

      fetch("/api/cars/" + self.car_id, {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
          Accept: "application/json",
        },
      })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {

        if ("car" in data) {
          let car = data.car;
          self.car = car;
          console.log(self.car);
        } else {
          self.car = {
              id: "",
              photo: "",
              year: "",
              make: "",
              model: "",
              description: "",
              colour: "",
              car_type: "",
              price: "",
              transmission: "",
          };
        }
      });

    },
    email() {
      console.log("cannot send email");
    },
    like() {
      let self = this;

      self.messages = [];
      self.msgClass = "";

      fetch("/api/cars/" + self.user_id + "/favourite", {
        method: "POST",
        headers: {
          "X-CSRFToken": self.csrf_token,
          Accept: "application/json",
        },
      })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
          console.log(data);

          if ("car_id" in data) {
            let like = document.getElementById("like-btn");
            like.style.backgroundColor = "DeepPink";
            console.log("data.message");

            self.messages = ["Car Favourited Successfully"];
            self.msgClass = "alert alert-success";
            console.log(self.messages);
          } else {
            self.messages = ["Error. Failed to save"];
            self.msgClass = "alert alert-danger";
            console.log(self.messages);
          }
      })
        .catch(function (error) {
          console.log(error);
      });
      
    },
    getCsrfToken() {
      let self = this;

      fetch("/api/csrf-token")
      .then((response) => response.json())
      .then((data) => {
        //console.log(data);
        self.csrf_token = data.csrf_token;
      });
    }
  } 
};

</script>

<style scoped>
.iconify-inline {
  font-size: 35px;
  padding: 6px;
  border-radius: 50%;
  margin: 0px;
}
.like {
  text-align: right;
}
.btn-circle {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  margin: 0px;
  padding: 2px;
}
.component {
  margin-top: 50px;
  width: 65%;
}
.msg__list {
  list-style: none;
}
.msg__item {
  display: inline-block;
  vertical-align: top;
}
button {
  width: 40%;
  margin-left: 10px;
}
.pill {
  width: fit-content;
  height: fit-content;
  margin: 1em 0em 1em 1em;
  color: white;
  font-size: small;
  padding: 0em 1em 0em 1em;
}
#messages {
    width: 65%;
    margin: 10px auto;
}
</style>
