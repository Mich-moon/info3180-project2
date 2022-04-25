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
                msgClass: '',
                logged_in: false
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
                //console.log(form_data);
                let form_data_json = JSON.stringify( Object.fromEntries(form_data.entries()) );
                //console.log(form_data_json);

                fetch("/api/auth/login", {
                    method: 'POST',
                    body: form_data_json,
                    headers: {
                    'X-CSRFToken': self.csrf_token,
                    'Accept' : 'application/json',
                    'Content-Type' : 'application/json'
                    }
                })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    console.log(data);

                    if ("errors" in data){
                        self.messages = data.errors;
                        self.msgClass = "alert alert-danger";
                        console.log(self.messages);
                    } else if ("token" in data) {
                        self.messages = ["Login Successful"];
                        self.msgClass = "alert alert-success";               
                        console.log(self.messages);
                        loginForm.reset();  // clear form

                        let jwt_token = data.token;

                        // We store this token in localStorage so that subsequent API requests
                        // can use the token until it expires or is deleted.
                        localStorage.setItem("token", JSON.stringify(jwt_token));
                        
                        self.logged_in = true;

                        // redirect to explore page
                        self.$router.push({ path: '/explore'});
                        //self.$router.push({name: '/explore', params: {}});
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

