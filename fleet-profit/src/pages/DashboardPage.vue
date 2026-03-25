<template>
  <q-page padding>
    <div v-if="alerts.length">
      <q-card class="q-pa-md q-mb-lg">
        <div class="text-h6 q-mb-md">🚨 Fleet Insights</div>

        <div v-for="(a, i) in alerts" :key="i" class="q-mb-sm">
          <q-chip color="red-2" text-color="red-10">
            {{ a }}
          </q-chip>
        </div>
      </q-card>
    </div>
    <!-- KPI CARDS -->

    <div class="row q-col-gutter-md q-mb-lg">
      <q-card class="col-3 bg-blue-6 text-white q-pa-md shadow-2 rounded-borders">
        <div class="text-subtitle2">Revenue</div>
        <div class="text-h4">₹ {{ kpi.revenue }}</div>
      </q-card>

      <q-card class="col-3 bg-red-5 text-white q-pa-md shadow-2 rounded-borders">
        <div class="text-subtitle2">Expense</div>
        <div class="text-h4">₹ {{ kpi.expense }}</div>
      </q-card>

      <q-card class="col-3 bg-green-6 text-white q-pa-md shadow-2 rounded-borders">
        <div class="text-subtitle2">Profit</div>
        <div class="text-h4">₹ {{ kpi.profit }}</div>
      </q-card>

      <q-card class="col-3 bg-purple-6 text-white q-pa-md shadow-2 rounded-borders">
        <div class="text-subtitle2">Margin</div>
        <div class="text-h4">{{ kpi.margin }} %</div>
      </q-card>
    </div>

    <!-- CHARTS -->

    <div class="row q-col-gutter-md q-mb-lg">
      <!-- DAILY REVENUE -->

      <q-card class="col-6 q-pa-md">
        <div class="text-h6 q-mb-md">Daily Revenue</div>

        <apexchart
          v-if="revenueSeries.length"
          type="line"
          height="300"
          :options="revenueChartOptions"
          :series="revenueSeries"
        />
      </q-card>

      <!-- VEHICLE PROFIT -->

      <q-card class="col-6 q-pa-md">
        <div class="text-h6 q-mb-md">Vehicle Profit</div>

        <apexchart
          v-if="vehicleSeries.length"
          type="bar"
          height="300"
          :options="vehicleChartOptions"
          :series="vehicleSeries"
        />
      </q-card>
    </div>

    <!-- VEHICLE TABLE -->

    <q-card class="q-pa-md q-mb-lg">
      <div class="text-h6 q-mb-md">Vehicle Performance</div>

      <q-table :rows="vehicles" :columns="vehicleColumns" row-key="vehicle_number" />
    </q-card>

    <!-- DRIVER TABLE -->

    <q-card class="q-pa-md">
      <div class="text-h6 q-mb-md">Driver Performance</div>

      <q-table :rows="drivers" :columns="driverColumns" row-key="driver_name" />
    </q-card>
    <div class="row q-col-gutter-md q-mb-lg">
      <q-card class="col-3 bg-grey-2 q-pa-md">
        <div class="text-subtitle2">Total Vehicles</div>
        <div class="text-h5">{{ vehicles.length }}</div>
      </q-card>

      <q-card class="col-3 bg-grey-2 q-pa-md">
        <div class="text-subtitle2">Total Drivers</div>
        <div class="text-h5">{{ drivers.length }}</div>
      </q-card>

      <q-card class="col-3 bg-grey-2 q-pa-md">
        <div class="text-subtitle2">Avg Profit / Vehicle</div>
        <div class="text-h5">₹ {{ Math.round(kpi.profit / vehicles.length) }}</div>
      </q-card>

      <q-card class="col-3 bg-grey-2 q-pa-md">
        <div class="text-subtitle2">Fuel Cost %</div>
        <div class="text-h5">{{ Math.round((kpi.expense / kpi.revenue) * 100) }} %</div>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import axios from 'axios'
import ApexChart from 'vue3-apexcharts'

export default {
  components: {
    apexchart: ApexChart,
  },

  data() {
    return {
      kpi: {},

      vehicles: [],
      drivers: [],
      alerts: [],

      revenueSeries: [],
      vehicleSeries: [],

      revenueChartOptions: {
        chart: {
          id: 'revenue',
          toolbar: { show: false },
        },
        stroke: {
          curve: 'smooth',
        },
        xaxis: {
          categories: [],
        },
      },

      vehicleChartOptions: {
        chart: {
          id: 'vehicle',
        },
        plotOptions: {
          bar: {
            borderRadius: 6,
          },
        },
        xaxis: {
          categories: [],
        },
      },

      vehicleColumns: [
        { name: 'vehicle_number', label: 'Vehicle', field: 'vehicle_number', align: 'left' },
        { name: 'vehicle_type', label: 'Type', field: 'vehicle_type' },
        { name: 'revenue', label: 'Revenue', field: 'revenue' },
        { name: 'fuel_cost', label: 'Fuel', field: 'fuel_cost' },
        { name: 'profit', label: 'Profit', field: 'profit' },
        { name: 'margin', label: 'Margin %', field: 'margin' },
      ],

      driverColumns: [
        { name: 'driver_name', label: 'Driver', field: 'driver_name', align: 'left' },
        { name: 'revenue', label: 'Revenue', field: 'revenue' },
        { name: 'fuel_cost', label: 'Fuel', field: 'fuel_cost' },
        { name: 'profit', label: 'Profit', field: 'profit' },
        { name: 'margin', label: 'Margin %', field: 'margin' },
      ],
    }
  },

  mounted() {
    this.loadDashboard()
  },

  methods: {
    async loadDashboard() {
      const res = await axios.get('http://localhost:5000/data')

      this.kpi = res.data.kpi
      this.vehicles = res.data.vehicle_summary
      this.drivers = res.data.driver_summary
      this.alerts = res.data.alerts
      /* DAILY REVENUE CHART */

      const daily = res.data.daily_revenue

      this.revenueSeries = [
        {
          name: 'Daily Revenue',
          data: daily.map((d) => d.revenue),
        },
      ]

      this.revenueChartOptions = {
        ...this.revenueChartOptions,
        xaxis: {
          categories: daily.map((d) => d.date),
        },
      }

      /* VEHICLE PROFIT CHART */

      const vehicles = res.data.vehicle_summary || []

      this.vehicleSeries = JSON.parse(
        JSON.stringify([
          {
            name: 'Vehicle Profit',
            data: vehicles.map((v) => Number(v.profit)),
          },
        ]),
      )

      this.vehicleChartOptions = JSON.parse(
        JSON.stringify({
          chart: {
            id: 'vehicle',
          },
          plotOptions: {
            bar: { borderRadius: 4 },
          },
          xaxis: {
            categories: vehicles.map((v) => v.vehicle_number + ' (' + v.vehicle_type + ')'),
          },
        }),
      )
    },
  },
}
</script>
