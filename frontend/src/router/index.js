import Vue from 'vue'
import VueRouter from 'vue-router'
import HomePage from '../views/HomePage.vue'
import MyProfile from '../views/MyProfile.vue'
import EditProfilePage from '../views/EditProfilePage.vue'

import TheatresDisplay from '../views/TheatresDisplay.vue'
import DisplayShows from '../views/DisplayShows.vue'

import MovieDisplay from '../views/MovieDisplay.vue'
import MovieShows from '../views/MovieShows.vue'
import FinalBooking from '../views/FinalBooking.vue'


import AdminLogin from '../views/AdminLogin.vue'
import AdminSignUp from '../views/AdminSignUp.vue'

import AdminHome from '../views/AdminHome.vue'
import AddTheatre from '../views/AddTheatre.vue'
import ManageTheatres from '../views/ManageTheatres.vue'

import ManageShows from '../views/ManageShows.vue'
import EditShow from '../views/EditShow.vue'




import EditTheatre from '../views/EditTheatre.vue'

import AddMovie from '../views/AddMovie.vue'
import AddShows from '../views/AddShows.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: "/",
    name: "HomePage",
    component: HomePage,
    meta: { requiresAuth: false }
  },

  {
    path: "/MyProfile",
    name: "MyProfile",
    component: MyProfile,
  
  },

  {
    path: "/EditProfilePage",
    name: "EditProfilePage",
    component: EditProfilePage,
  
  },

  {
    path: "/TheatresDisplay",
    name: "TheatresDisplay",
    component: TheatresDisplay,
  
  },

  {
    path: "/DisplayShows/:theatreId",
    name: "DisplayShows",
    component: DisplayShows,
  
  },

  {
    path: '/movies/:movieName',
    name: 'MovieDisplay',
    component: MovieDisplay,
    props: true,
  },

  {
    path: '/MovieShows/:movieName',
    name: 'MovieShows',
    component: MovieShows,
  },

{
    path: '/FinalBooking/:showId',
    name: 'FinalBooking',
    component: FinalBooking,
    props: true,
  },

  {
    path: "/admin",
    name: "AdminLogin",
    component: AdminLogin,
  },

  {
    path: "/admin/signup",
    name: "AdminSignUp",
    component: AdminSignUp,
  },

  {
    path: "/admin/Home",
    name: "AdminHome",
    component: AdminHome,
  },

  {
    path: "/admin/AddTheatre",
    name: "AddTheatre",
    component: AddTheatre,
    meta: { requiresAuth: true }, // Add the meta field to indicate authentication is required
   
  },

  

  {
    path: "/admin/Managetheatres",
    name: "ManageTheatres",
    component: ManageTheatres,
    // meta: { requiresAuth: true }, // Add the meta field to indicate authentication is required
   
  },

  {
    path: "/admin/EditTheatre/:theatre_id",
    name: "EditTheatre",
    component: EditTheatre,
    // meta: { requiresAuth: true }, // Add the meta field to indicate authentication is required
   
  },

  {
    path: "/admin/ManageShows",
    name: "ManageShows",
    component: ManageShows,
    // meta: { requiresAuth: true }, // Add the meta field to indicate authentication is required
   
  },

  {
    path: "/admin/EditShow/:show_id/:theatreId",
    name: "EditShow",
    component: EditShow,
    // meta: { requiresAuth: true }, // Add the meta field to indicate authentication is required
    props: true
   
  },

  {
    path: "/admin/Addmovie",
    name: "Addmovie",
    component: AddMovie,
  },

  
  {
    path: "/admin/AddShows",
    name: "AddShows",
    component: AddShows,
  },
  // {
  //   path: "/",
  //   name: "home",
  //   component: HomeView,
  // },

    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    // }
]

export function getAuthToken() {
  return localStorage.getItem('access_token'); // Replace 'jwt' with the key you use to store the JWT
}

// // Check if the JWT is present and valid before each navigation
// router.beforeEach((to, from, next) => {
//   const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
//   const authToken = getAuthToken(); // Implement this function to retrieve the JWT from local storage

//   if (requiresAuth && !authToken) {
//     // Redirect to the login page or display an error message
//     next('/HomePage');
//   } else {
//     // Allow the navigation
//     next();
//   }
// });




const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
