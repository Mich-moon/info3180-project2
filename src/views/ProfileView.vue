<template>
    <div class="container-fluid d-flex flex-column">
        <div class="row px-0 component mb-5 px-2">
            <div class="col-4 mx-0 p-2">
                <img class="card-img-top rounded-circle" :src="photo_url" />
            </div>
            <div class="col-8 mx-0 p-2">
                <div>
                    <h3>{{ user.name }}</h3>
                    <h5 class="grey">&#64;{{ user.username }}</h5>
                    <p class="py-4 grey">{{ user.biography }}</p>
                    <p><span class="grey">Email: </span><span class="fw-bold"> {{ user.email }}</span></p>
                    <p><span class="grey">Location: </span><span class="fw-bold"> {{ user.location }}</span></p>
                    <p><span class="grey">Joined: </span><span class="fw-bold"> {{ user.date_joined }}</span></p> 
                </div>
            </div>
        </div>

        <div class="form-head">
            <h1>Cars Favourited</h1>
        </div>
        <hr/>
        <div id="results" :v-if="results" class="results scroller">
            <CarCard :v-if="results" v-for= "c in results" :key= "c.id" 
				:id= "c.id"  
                :photo = "c.photo"
			    :make = "c.make"
			    :model = "c.model"
			    :year = "c.year" 
			    :price = "c.price"
        	/>
        </div>
    </div>
</template>

<script>
    import CarCard from '@/components/CarCard.vue'

    export default {
        components: { CarCard },
        data() {
            return {
                csrf_token: "",
                id: null,
                user: {},
                results: [],
                photo_url: 'https://frameartjamaica.com/wp-content/uploads/2018/07/placeholder-img-1.jpg'
            };
        },
        created() {
            this.isLoggedIn();
            this.getCsrfToken();
            this.getUser();
            this.getFavourites();
        },
        methods: {
            isLoggedIn() {
                let self = this;

                if (localStorage.getItem("token")) {
                    self.logged_in = true;

                    // retrieve user id from token stored in localstorage
                    let jwt_token = JSON.parse( localStorage.getItem("token") );

                    var base64Url = jwt_token.split('.')[1];
                    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
                    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
                        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                    }).join(''));

                    let jwt_payload = JSON.parse(jsonPayload);
                    self.id = jwt_payload['sub'];

                } else {
                    // redirect to home page
                    self.$router.push({ path: '/'});
                }
            },
            getUser() {
                let self = this;

                fetch("/api/users/" + self.id, {
                    headers: {
                        Authorization: "Bearer " + localStorage.getItem("token"),
                        'X-CSRFToken': self.csrf_token
                    },
                })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    console.log(data);

                    if ("user" in data) {
                        self.user = data.user;
                    } else {
                        self.user = {
                            "id": "",
                            "photo": "",
                            "name": "",
                            "username": "",
                            "biography": "",
                            "email": "",
                            "location": "",
                            "date_joined": "",
                        };
                    }
                });

                if (self.user.id != "") {
                    fetch("/api/uploads/?filename=" + self.user.photo)
                    .then((response) => response.json())
                    .then((data) => {
                        if ("path" in data) {
                            console.log(data.path);
                            self.photo_url = data.path;
                        } 
                    })
                }

            },
            getFavourites(){
                let self = this;

                fetch("/api/users/" + self.id + "/favourites", {
                    headers: {
                        "Authorization" : "Bearer " + localStorage.getItem("token")
                    }
                })
                .then(function (response) {
                    console.log(response);
                    return response.json();
                })
                .then(function (data) {
                    console.log(data);

                    if ("favourites" in data) {
                        self.results = data.favourites;
                    } else {
                        self.results =  [{
                            'id': '',
                            'photo': 'https://frameartjamaica.com/wp-content/uploads/2018/07/placeholder-img-1.jpg', 
                            'year': '', 
                            'make': '', 
                            'model': '', 
                            'price': ''
                        }];
                    }
                })
                .catch(function (error) {
                    self.results = [error];
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
            },
        },
    };
</script>

<style scoped>
.component {
    margin-top: 50px;
    width: 65%;
}
.form-head {
    width: 70%;
    margin-bottom: 0px;;
}
.results {
    width:70%;
    margin: 0 auto;
    padding: 30px;
}
.scroller {
    overflow-y: scroll;
    scrollbar-color: rebeccapurple green;
    scrollbar-width: thin;
}
.msg__list {
    list-style: none;
}
.msg__item {
    display: inline-block;
    vertical-align: top;
}
.grey{
  color: grey;
}
hr {
    width: 75%;
    margin: 20px auto;
}
</style>
