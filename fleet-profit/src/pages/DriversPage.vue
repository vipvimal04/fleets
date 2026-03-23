<template>

<q-page padding>

<q-table
title="Driver Performance"
:rows="drivers"
:columns="columns"
/>

</q-page>

</template>

<script>

import axios from "axios"

export default {

data() {

return {

drivers: [],

columns: [

{ name:"driver_name", label:"Driver", field:"driver_name" },

{ name:"revenue", label:"Revenue", field:"revenue" },

{ name:"fuel_cost", label:"Fuel", field:"fuel_cost" },

{ name:"profit", label:"Profit", field:"profit" },

{ name:"margin", label:"Margin %", field:"margin" }

]

}

},

mounted() {

this.loadDrivers()

},

methods: {

async loadDrivers(){

const res = await axios.get("http://localhost:5000/data")

this.drivers = res.data.driver_summary

}

}

}

</script>