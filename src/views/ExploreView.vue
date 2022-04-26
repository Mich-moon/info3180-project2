<template>
    <div class="container-fluid d-flex flex-column">

        <div id="messages" :class="msgClass" :v-if="msgClass">
            <ul class="msg__list">
                <li v-for="(message, index) in messages" :key="index" class="msg__item">  
                    {{ message }}
                </li>
            </ul>
        </div>

        <div class="form-head">
            <h1>Explore</h1>
        </div>
        <form @submit.prevent="search" id="searchForm" class="component mb-5 ">

            <div class="form-group">
                <div class="form-control">
                    <label class="" for="make">Make</label>
                    <input name="make" id="make"/>
                </div>
                <div class="form-control">
                    <label class="" for="model">Model</label>
                    <input name="model" id="model"/>
                </div>
                <button class="btn btn-success mb-2">Search</button>
            </div>
        </form>
        <hr/>
        <div id="results" :v-if="results" class="results">
            <CarCard :v-if="results" v-for= "c in results" class="carcard" :key= "c.id" 
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
                csrf_token: '',
                search_path: '',
                results: [],
                messages: [],
                msgClass: ''
            }
        },
        created() {
            this.isLoggedIn();
            this.getCsrfToken();
            this.getCars();
        },
        methods: {
            isLoggedIn() {
              let self = this;

              if (localStorage.getItem("token")) {
                self.logged_in = true;
                
              } else {
                // redirect to home page
                self.$router.push({ path: '/'});
              }
            },
            getCars() {
                let self = this;

                self.messages = [];
                self.msgClass = "";

                fetch("/api/cars", {
                    headers: {
                        'Authorization' : 'Bearer ' + localStorage.getItem("token")
                    },
                })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    if ("cars" in data) {
                        //console.log(data);
                        let cars = data.cars;
                        console.log(cars);

                        if (cars.length > 3) {
                            self.results = cars.slice(0,3);
                        } else {
                            self.results = cars;
                        }
                        
                        //self.results = JSON.stringify(data.cars);
                        //self.results = JSON.parse(data.cars).slice(0,2);
                        //self.results = JSON.parse(data.cars);
                        console.log(self.results);

                    } else if ("message" in data) {
                        self.messages = [data.message];
                        self.msgClass = "alert alert-danger";
                    } 
                })
                .catch(function (error) {
                    self.messages = ["Oops. Something went wrong"];
                    self.msgClass = "alert alert-danger";
                    console.log(error);
                });

            },
            search() {
                let self = this;

                self.messages = [];
                self.msgClass = "";

                let make = document.getElementById('make').value;
                let model = document.getElementById('model').value;

                console.log(make);
                console.log(model);

                if (make == '' && model == '') {
                  self.search_path = "/api/search";

                } else if (make.length == 0) {
                  self.search_path = "/api/search/?model=" +  model;

                } else if (model.length == 0) {
                  self.search_path = "/api/search/?make=" +  make;

                } else {
                  self.search_path = "/api/search/?make=" +  make + "&model=" + model;

                }

                fetch(self.search_path, {
                    headers: {
                        'Authorization' : 'Bearer ' + localStorage.getItem("token")
                    }
                })
                .then(function (response) {
                    console.log(response);
                    return response.json();
                })
                .then(function (data) {
                    if ("cars" in data) {
                        elf.messages = [data.cars.length + "cars found"];
                        self.msgClass = "alert alert-success";
                        
                        console.log(data);
                        self.results = JSON.parse(data.cars);
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
                //console.log(data);
                self.csrf_token = data.csrf_token;
                })
            }
        }
    };
</script>

<style scoped>
.component {
    width: 65%;
}
.form-head {
    width: 70%;
}
.results {
    width:70%;
    margin: 0 auto;
    padding: 30px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-gap: 5px;
}
button {
    margin: auto 0px 0px 10px;
    width: 85%;
}
.form-group {
    grid-template-columns: 2fr 2fr 1fr;
}
hr {
    width: 75%;
    margin: 20px auto;
}
.msg__list {
    list-style: none;
}
.carcard {
    width: 100%;
}
</style>