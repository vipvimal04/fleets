const routes = [

  {
  path: '/',
  component: () => import('layouts/MainLayout.vue'),
  
  children: [
  
  { path: '', component: () => import('pages/DashboardPage.vue') },
  
  { path: 'vehicles', component: () => import('pages/VehiclesPage.vue') },
  
  { path: 'drivers', component: () => import('pages/DriversPage.vue') },
  
  { path: 'upload', component: () => import('pages/UploadPage.vue') }
  
  ]
  
  }
  
  ]
  
  export default routes