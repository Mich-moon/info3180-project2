<template>
  <div class="container-fluid d-flex flex-column">

    <div class="form-head">
      <h1>Register New User</h1>
    </div>
    <form @submit.prevent="register" id="registerForm" class="component mb-5 ">

        <div id="messages" :class="msgClass" :v-if="msgClass">
            <ul class="msg__list">
                <li v-for="(message, index) in messages" :key="index" class="msg__item">  
                    {{ message }}
                </li>
            </ul>
        </div>

        <div class="form-group">
            <div class="form-control">
                <label class="" for="username">Username</label>
                <input name="username" id="username" required/>
            </div>
            <div class="form-control">
                <label class="" for="password">Password</label>
                <input type="password" name="password" id="password" required/>
            </div>
        </div>
        <div class="form-group">
            <div class="form-control">
                <label class="" for="fullname">Fullname</label>
                <input name="fullname" id="fullname" required/>
            </div>
            <div class="form-control">
                <label class="" for="email">Email</label>
                <input type="email" name="email" id="email" required/>
            </div>
        </div>
        <div class="form-group">
            <div class="form-control">
                <label class="" for="location">Location</label>
                <input name="location" id="location" required/>
            </div>
        </div>
        <div class="form-control">
            <label class="" for="biography">Biography</label>
            <textarea name="biography" id="biography" rows="5" required></textarea>
        </div>
        <div class="form-control">
            <label class="" for="photo">Image Upload</label>
            <input type="file" name="photo"/>
        </div>
        <div class="form-control">
            <button class="btn btn-success mb-2">Register</button>
        </div>

    </form>
  </div>
</template>

<script>
    export default {
        data() {
            return {
                csrf_token: '',
                messages: [],
                msgClass: ''
            }
        },
        created() {
            this.getCsrfToken();
        },
        methods: {
            register() {
                let self = this;

                self.messages = [];
                self.msgClass = "";

                let registerForm = document.getElementById('registerForm');
                let form_data = new FormData(registerForm);

                fetch("/api/register", {
                    method: 'POST',
                    body: form_data,
                    headers: {
                    'Accept' : 'application/json',
                    'Content-Type' : 'application/json',
                    'X-CSRFToken': self.csrf_token
                    }
                })
                .then(function (response) {
                    console.log(response);
                    return response.json();
                })
                .then(function (data) {
                    console.log(data);

                    if ("errors" in data){
                        self.messages = data.errors;
                        self.msgClass = "alert alert-danger";
                        console.log(self.messages);
                    } else {
                        self.messages = ["Registration Successful"];
                        self.msgClass = "alert alert-success";               
                        console.log(self.messages);
                        registerForm.reset();  // clear form
                    }
                })
                .catch(function (error) {
                    self.messages = ["Oops. Something went wrong"];
                    self.msgClass = "alert alert-danger";
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
        }
    };
</script>

<style scoped>
.msg__list {
    list-style: none;
}
</style>

