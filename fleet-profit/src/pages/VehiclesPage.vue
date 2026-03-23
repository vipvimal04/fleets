<template>

<q-page padding>

<q-table
title="Vehicle Profit Report"
:rows="vehicles"
:columns="columns"
/>

</q-page>

</template>

<script>

import axios from "axios"

export default {

data() {

return {

vehicles: [],

columns: [

{ name:"vehicle_number", label:"Vehicle", field:"vehicle_number" },

{ name:"vehicle_type", label:"Type", field:"vehicle_type" },

{ name:"revenue", label:"Revenue", field:"revenue" },

{ name:"fuel_cost", label:"Fuel", field:"fuel_cost" },

{ name:"profit", label:"Profit", field:"profit" },

{ name:"margin", label:"Margin %", field:"margin" }

]

}

},

mounted() {

this.loadVehicles()

},

methods: {

async loadVehicles(){

const res = await axios.get("http://localhost:5000/data")

this.vehicles = res.data.vehicle_summary

}

}

}

</script>