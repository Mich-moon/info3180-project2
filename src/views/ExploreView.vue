<template>
    <div class="container-fluid d-flex flex-column">

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
                csrf_token: '',
                search_path: '',
                results: []
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

                fetch("/api/cars", {
                    method: 'GET',
                    headers: {
                        'Authorization' : 'Bearer ' + localStorage.getItem("token"),
                        'X-CSRFToken': self.csrf_token
                    },
                })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    if ("cars" in data) {
                        console.log(data);
                        self.results = JSON.parse(data.cars).slice(0,2);
                    } else {
                        self.results =  [{
                            'id': '',
                            'photo': '', 
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
            search() {
                let self = this;

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
                        'Authorization' : 'Bearer ' + localStorage.getItem("token"),
                        'X-CSRFToken' : self.csrf_token
                    }
                })
                .then(function (response) {
                    console.log(response);
                    return response.json();
                })
                .then(function (data) {
                    if ("cars" in data) {
                        console.log(data);
                        self.results = JSON.parse(data.cars);
                    } else {
                        self.results =  [{
                            'id': '',
                            'photo': '', 
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
}
button {
    margin: auto 0px 0px 10px;
    width: 85%;
}
.form-group {
    grid-template-columns: 2fr 2fr 1fr;
}
.scroller {
    overflow-y: scroll;
    scrollbar-color: rebeccapurple green;
    scrollbar-width: thin;
}
hr {
    width: 75%;
    margin: 20px auto;
}
</style>