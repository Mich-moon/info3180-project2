<template>
  <div class="container-fluid d-flex flex-column">

    <div class="form-head">
      <h1>Add New Car</h1>
    </div>
    <form @submit.prevent="add_car" id="carForm" class="component mb-5 ">

        <div id="messages" :class="msgClass" :v-if="msgClass">
            <ul class="msg__list">
                <li v-for="(message, index) in messages" :key="index" class="msg__item">  
                    {{ message }}
                </li>
            </ul>
        </div>

        <div class="form-group">
            <div class="form-control">
                <label class="" for="make">Make</label>
                <input name="make" id="make" required/>
            </div>
            <div class="form-control">
                <label class="" for="model">Model</label>
                <input name="model" id="model" required/>
            </div>
        </div>
        <div class="form-group">
            <div class="form-control">
                <label class="" for="colour">Colour</label>
                <input name="colour" id="colour" required/>
            </div>
            <div class="form-control">
                <label class="" for="year">year</label>
                <input type="number" name="year" id="year" required/>
            </div>
        </div>
        <div class="form-group">
            <div class="form-control">
                <label class="" for="price">Price</label>
                <input type="number" step=".01" name="price" id="price" required/>
            </div>
            <div class="form-control">
                <label class="" for="cartype">Car Type</label>
                <select name="cartype" id="cartype" required>
                  <option value="suv">SUV</option>
                  <option value="pickup truck">Pickup Truck</option>
                  <option value="convertible">Convertible</option>
                  <option value="coupe">Coupe</option>
                  <option value="muv">MUV</option>
                  <option value="sedan">Sedan</option>
                  <option value="hatchback">Hatchback</option>
                </select>
            </div>
        </div>
        <div class="form-group">
            <div class="form-control">
                <label class="" for="transmission">Transmission</label>
                <select name="transmission" id="transmission" required>
                  <option value="automatic">Automatic</option>
                  <option value="manual">Manual</option>
                  <option value="continuously variable">Continuously variable</option>
                  <option value="semi-automatic and dual-clutch">Semi-automatic and dual-clutch</option>
                </select>
            </div>
        </div>
        <div class="form-control">
            <label class="" for="description">Description</label>
            <textarea name="description" id="description" rows="5" required></textarea>
        </div>
        <div class="form-control">
            <label class="" for="photo">Upload Photo</label>
            <input type="file" name="photo"/>
        </div>
        <div class="form-control">
            <button class="btn btn-success mb-2">Save</button>
        </div>

        <input type="hidden" id="user_id" name="user_id" :value="id"/>

    </form>
  </div>
</template>

<script>
    export default {
        data() {
            return {
                csrf_token: '',
                logged_in: false,
                messages: [],
                msgClass: '',
                id: null
            }
        },
        created() {
            this.isLoggedIn();
            this.getCsrfToken();
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
                    self.id = jwt_payload['sub'];

                } else {
                    self.logged_in = false;
                    // redirect to home page
                    self.$router.push({ path: '/'});
                }
            },
            add_car() {
                let self = this;

                self.messages = [];
                self.msgClass = "";

                let carForm = document.getElementById('carForm');
                let form_data = new FormData(carForm);

                console.log(self.csrf_token);

                fetch("/api/cars", {
                    method: 'POST',
                    body: form_data,
                    headers: {
                        'Authorization' : 'Bearer ' + localStorage.getItem("token"),
                        'Accept' : 'application/json',
                        'Content-Type' : 'application/json',
                        'X-CSRFToken': self.csrf_token
                    }
                })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    // display a success message
                    console.log(data);

                    if ("error" in data){
                        self.messages = data.error;
                        self.msgClass = "alert alert-danger";
                        console.log(self.messages);
                    } else {
                        self.messages = ["Car Added Successfully"];
                        self.msgClass = "alert alert-success";               
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
                console.log(data);
                self.csrf_token = data.csrf_token;
                })
            }
        },
    };
</script>

<style scoped>
.msg__list {
    list-style: none;
}
.msg__item {
  display: inline-block;
  vertical-align: top;
}
</style>

