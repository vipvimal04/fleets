<template>

<q-page padding>

<q-file
filled
label="Upload Fleet Excel"
@update:model-value="uploadFile"
/>

<br>

<!-- SUMMARY CARDS -->

<div class="row q-col-gutter-md">

<q-card class="col">
<q-card-section>
<div class="text-subtitle2">Revenue</div>
<div class="text-h6">₹ {{summary.revenue}}</div>
</q-card-section>
</q-card>

<q-card class="col">
<q-card-section>
<div class="text-subtitle2">Expense</div>
<div class="text-h6">₹ {{summary.expense}}</div>
</q-card-section>
</q-card>

<q-card class="col">
<q-card-section>
<div class="text-subtitle2">Profit</div>
<div class="text-h6">₹ {{summary.profit}}</div>
</q-card-section>
</q-card>

<q-card class="col">
<q-card-section>
<div class="text-subtitle2">Margin</div>
<div class="text-h6">{{summary.margin}} %</div>
</q-card-section>
</q-card>

</div>

<br>

<!-- TOP VEHICLE -->

<q-banner class="bg-green text-white">
🏆 Top Vehicle: {{topVehicle["Vehicle Number"]}}
Profit ₹{{topVehicle["Profit"]}}
</q-banner>

<br>

<!-- WORST VEHICLE -->

<q-banner class="bg-red text-white">
⚠ Worst Vehicle: {{worstVehicle["Vehicle Number"]}}
Profit ₹{{worstVehicle["Profit"]}}
</q-banner>

<br>

<!-- ALERTS -->

<q-banner
v-if="alerts.length"
class="bg-orange text-black"
>
⚠ {{alerts[0]}}
</q-banner>

<br>

<!-- VEHICLE PROFIT CHART -->

<q-card>
<q-card-section>
<div class="text-h6">Vehicle Profit</div>
<canvas id="vehicleChart"></canvas>
</q-card-section>
</q-card>

<br>

<!-- DIESEL TABLE -->

<q-table
title="Diesel Efficiency"
:rows="diesel"
:columns="columns"
row-key="Vehicle Number"
/>

</q-page>

</template>

<script>

import axios from "axios"
import Chart from "chart.js/auto"

export default {

data(){
return{

summary:{},
vehicles:[],
diesel:[],
alerts:[],

topVehicle:{},
worstVehicle:{},

vehicleChart:null,

columns:[
{
name:"vehicle",
label:"Vehicle",
field:"Vehicle Number"
},
{
name:"diesel",
label:"Diesel Expense",
field:"Diesel Expense"
},
{
name:"percent",
label:"Diesel %",
field:"Diesel %"
}
]

}
},

methods:{

uploadFile(file){

const formData = new FormData()
formData.append("file",file)

axios.post("http://127.0.0.1:5000/upload",formData)
.then(res=>{

this.summary = res.data.summary
this.vehicles = res.data.vehicles
this.diesel = res.data.diesel
this.alerts = res.data.alerts

this.topVehicle = res.data.top_vehicle
this.worstVehicle = res.data.worst_vehicle

this.renderChart()

})

},

renderChart(){

const labels = this.vehicles.map(v=>v["Vehicle Number"])
const profits = this.vehicles.map(v=>v["Profit"])

if(this.vehicleChart){
this.vehicleChart.destroy()
}

this.vehicleChart = new Chart(
document.getElementById("vehicleChart"),
{
type:"bar",
data:{
labels:labels,
datasets:[
{
label:"Profit",
data:profits
}
]
}
}
)

}

}

}

</script>