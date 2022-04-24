<template>
    <div class="container-fluid d-flex flex-column">

        <div class="form-head">
            <h1>Explore</h1>
        </div>
        <form @submit.prevent="search" id="searchForm" class="component mb-5 ">

            <div class="form-group">
                <div class="form-control">
                    <label class="" for="make">Make</label>
                    <input v-model="make" name="make" id="make"/>
                </div>
                <div class="form-control">
                    <label class="" for="model">Model</label>
                    <input v-model="model" name="model" id="model"/>
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
                make: '',
                model: '',
                search_path: '',
                results: [{
                    'id': 0,
                    'photo': '', 
                    'year': 2019, 
                    'make': 'Honda', 
                    'model': 'Civic', 
                    'price': 7000.00
                }]
                //results: []
            }
        },
        created() {
          this.isLoggedIn();
        },
        methods: {
            isLoggedIn() {
              let self = this;

              if (localStorage.getItem("token")) {
                self.logged_in = true;

              } else {
                self.logged_in = false;
              }
            },
            search() {
                let self = this;

                if (make.length == 0 && model.length == 0) {
                  self.search_path = "/api/search" +  id;

                } else if (make.length == 0) {
                  self.search_path = "/api/search/?model=" +  self.model;

                } else if (model.length == 0) {
                  self.search_path = "/api/search/?make=" +  self.make;

                } else {
                  self.search_path = "/api/search/?make=" +  self.make + "&model=" + self.model;

                }

                fetch(self.search_path, {
                    method: 'GET',
                    headers: {
                        "Authorization" : "Bearer " + localStorage.getItem("token"),
                        "Accept" : "application/json"
                    }
                })
                .then(function (response) {
                    console.log(response);
                    return response.json();
                })
                .then(function (data) {
                    console.log(data);

                    this.results = JSON.parse(data.results);
                })
                .catch(function (error) {
                    self.results = [error];
                    console.log(error);
                });

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