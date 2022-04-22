<template>
  <div class="container-fluid d-flex flex-column">

    <div class="form-head">
      <h1>Login to your account</h1>
    </div>
    <form @submit.prevent="login" id="loginForm" class="component mb-5">

        <div id="messages" :class="msgClass" :v-if="msgClass">
            <ul class="msg__list">
                <li v-for="(message, index) in messages" :key="index" class="msg__item">  
                    {{ message }}
                </li>
            </ul>
        </div>

        <div class="form-control">
            <label class="" for="username">Username</label>
            <input name="username" id="username" required/>
        </div>
        <div class="form-control">
            <label class="" for="password">Password</label>
            <input type="password" name="password" id="password" required/>
        </div>
      
        <div class="form-control">
            <button class="btn btn-success mb-2">Login</button>
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
            login() {
                let self = this;

                self.messages = [];
                self.msgClass = "";

                let loginForm = document.getElementById('loginForm');
                let form_data = new FormData(loginForm);

                fetch("/api/auth/login", {
                    method: 'POST',
                    body: form_data,
                    headers: {
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
                        self.messages = ["Login Failed"];
                        self.msgClass = "alert alert-danger";
                        console.log(self.messages);
                    } else if ("token" in data) {
                        self.messages = ["Login Successful"];
                        self.msgClass = "alert alert-success";               
                        console.log(self.messages);

                        let jwt_token = data.token;

                        // We store this token in localStorage so that subsequent API requests
                        // can use the token until it expires or is deleted.
                        localStorage.setItem("token", jwt_token);

                        // redirect to explore page
                        self.$router.push({ path: '/explore'});
                        //self.$router.push({name: '/explore', params: {}});
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
.component {
    width:30%;
}
.form-head {
    margin: 0 32%;
}
</style>

