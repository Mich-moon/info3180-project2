<template>
    <div class="col-4 mx-0 p-2">
        <div class="card shadow-sm">
            <img
            class="card-img-top"
            :src="'/uploads/' + photo"
            />

            <div class="card-body">
                <h5>{{ year }} {{ make }}
                <span
                    class="rounded-pill pill fw-light"
                >
                    <span class="iconify-inline" data-icon="uil:pricetag-alt"></span>
                    {{ price }}
                </span>
                </h5>
                <p>{{ model }}</p>
            </div>
            <button @click.prevent="more" class="btn btn-primary mb-2">View more details</button>
        </div>
    </div>
</template>

<script>
	export default {
		props: ['id', 'photo', 'year', 'make', 'model', 'price'],
        methods: {
            more() {
                let self = this;
                // redirect to car view page
                self.$router.push({ name: 'car', params: { car_id: self.id } });
                //self.$router.push({ path: '/cars/' + self.id});
            }

        }
	}
</script>

<style scoped>
.card p {
    color: rgb(143, 142, 142);
}
.pill {
    width: fit-content;
    height: fit-content;
    margin: 1em 0em 1em 1em;
    color: white;
    font-size: medium;
    padding: 0em 1em 0em 1em;
    background-color: rgb(30, 206, 153);
}
button {
    margin: 0px 20px 20px 20px;
}
</style>