<template>
  <q-layout view="lHh Lpr lFf">

    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          Trinity Fleets Dashboard
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer show-if-above bordered>

      <q-list>

        <q-item clickable to="/">
          <q-item-section>Dashboard</q-item-section>
        </q-item>

        <q-item clickable to="/vehicles">
          <q-item-section>Vehicles</q-item-section>
        </q-item>

        <q-item clickable to="/drivers">
          <q-item-section>Drivers</q-item-section>
        </q-item>

        <q-item clickable to="/upload">
          <q-item-section>Upload Excel</q-item-section>
        </q-item>

      </q-list>

    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>