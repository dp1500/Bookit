
<template>
  <div> 
    <div class="wrapper">
    <!-- Sidebar  -->
    <nav id="sidebar">
        <div class="sidebar-header">
            <h3>BookIt</h3>
        </div>

        <ul class="list-unstyled components">
            <p>HOME</p>

            <li>
                <router-link to="/admin/AddTheatre">Add Theatre</router-link>
            </li>

            <li>
                <router-link to="/admin/ManageTheatres"> Manage Theatres</router-link>
            </li>

            <li>
                <router-link to="/admin/AddShows">Add Shows</router-link>
            </li>

            <li>
                <router-link to="/admin/manageShows">Manage Shows</router-link>
            </li>

            <li>
                <router-link to="/admin/AddMovie">Add Movie</router-link>
            </li>

           
        </ul>
      
    </nav>

    <!-- Page Content  -->
    <div  id="app">

    <div ref="contentOnly" id="content">
      
      <div class="dashboard">
        <div class="statistics">
          <div class="card">
            <div class="card-body">
              <h4 class="card-title">Top Theatre (Revenue)</h4>
              <p class="card-text">{{ topTheatreRevenue  }}</p>
            </div>
          </div>
          <div class="card">
            <div class="card-body">
              <h4 class="card-title">Total Bookings</h4>
              <p class="card-text">{{ totalBookings  }}</p>
            </div>
          </div>
          <div class="card">
            <div class="card-body">
              <h4 class="card-title">Total Revenue</h4>
              <p class="card-text">{{ totalRevenue  }}</p>
            </div>
          </div>
          <div class="card">
            <div class="card-body">
              <h4 class="card-title">Top Theatre (Bookings)</h4>
              <p class="card-text">{{ topTheatreBookings  }}</p>
            </div>
          </div>
        </div>

        <!-- <div class="charts">
          <div class="growth-chart">
            <img src="path_to_growth_chart_image" alt="Sales Chart" />
          </div>
          <div class="revenue-chart">
            <img src="path_to_revenue_chart_image" alt="Revenue Chart" />
          </div>
        </div> -->

        <div class="charts">
          <div class="revenue-chart">
            <h3>Revenue by Theatre</h3>
            <img :src="revenuePerTheatreChartLink" alt="Revenue Per Theatre Chart" />
          </div>
          <div class="growth-chart">
            <h3>Monthly Revenue</h3>
            <img :src="revenuePerMonthChartLink" alt="Monthly Revenue Chart" />
          </div>
        </div>

      </div>
      </div>
      <hr>
    </div>
          <div class="fixed-bottom d-flex justify-content-end mb-3 mr-3">
            <button class="btn btn-primary btn-sm" @click="generatePDF">Generate PDF</button>
          </div>

          

    </div>
    <div v-if="response_message"
              class= "alert alert-warning alert-dismissible fade show mt-2"
              role="alert">
                <strong> {{ response_message }} </strong>
            </div>
  </div>


</template>



<style >

/*
DEMO STYLE
*/

@import "https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700";
body {
font-family: 'Poppins', sans-serif;
background: #fafafa;
}

p {
font-family: 'Poppins', sans-serif;
font-size: 1.1em;
font-weight: 300;
line-height: 1.7em;
color: #999;
}

a,
a:hover,
a:focus {
color: inherit;
text-decoration: none;
transition: all 0.3s;
}

.navbar {
padding: 15px 10px;
background: #fff;
border: none;
border-radius: 0;
margin-bottom: 40px;
box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}

.navbar-btn {
box-shadow: none;
outline: none !important;
border: none;
}

.line {
width: 100%;
height: 1px;
border-bottom: 1px dashed #ddd;
margin: 40px 0;
}

/* ---------------------------------------------------
SIDEBAR STYLE
----------------------------------------------------- */

.wrapper {
display: flex;
width: 100%;
align-items: stretch;
}

#sidebar {
min-width: 250px;
max-width: 250px;
background: #7386D5;
color: #fff;
transition: all 0.3s;
}

#sidebar.active {
margin-left: -250px;
}

#sidebar .sidebar-header {
padding: 20px;
background: #6d7fcc;
}

#sidebar ul.components {
padding: 20px 0;
border-bottom: 1px solid #47748b;
}

#sidebar ul p {
color: #fff;
padding: 10px;
}

#sidebar ul li a {
padding: 10px;
font-size: 1.1em;
display: block;
}

#sidebar ul li a:hover {
color: #7386D5;
background: #fff;
}

#sidebar ul li.active>a,
a[aria-expanded="true"] {
color: #fff;
background: #6d7fcc;
}

a[data-toggle="collapse"] {
position: relative;
}

.dropdown-toggle::after {
display: block;
position: absolute;
top: 50%;
right: 20px;
transform: translateY(-50%);
}

ul ul a {
font-size: 0.9em !important;
padding-left: 30px !important;
background: #6d7fcc;
}

ul.CTAs {
padding: 20px;
}

ul.CTAs a {
text-align: center;
font-size: 0.9em !important;
display: block;
border-radius: 5px;
margin-bottom: 5px;
}

a.download {
background: #fff;
color: #7386D5;
}

a.article,
a.article:hover {
background: #6d7fcc !important;
color: #fff !important;
}

/* ---------------------------------------------------
CONTENT STYLE
----------------------------------------------------- */

#content {
width: 100%;
padding: 20px;
min-height: 100vh;
transition: all 0.3s;
}

/* ---------------------------------------------------
MEDIAQUERIES
----------------------------------------------------- */

@media (max-width: 768px) {
#sidebar {
    margin-left: -250px;
}
#sidebar.active {
    margin-left: 0;
}
#sidebarCollapse span {
    display: none;
}
}



.dashboard {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    width: 100%;
    height: 100%;
  }

  .statistics {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
  }

  .statistic-item {
    flex: 1;
    background-color: #f1f1f1;
    padding: 20px;
    border-radius: 5px;
  }

  .statistic-item-inner {
    text-align: center;
  }

  /* .charts {
    display: flex;
    justify-content: space-between;
    height: 100%;
  } */

  /* .growth-chart {
    flex: 2;
    background-color: #f1f1f1;
    padding: 20px;
    border-radius: 5px;
  }

  .revenue-chart {
    flex: 1;
    background-color: #f1f1f1;
    padding: 20px;
    border-radius: 5px;
  } */

  .charts {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: stretch;
}


  .revenue-chart {
    max-width: 100%;
    height: auto;
  flex: 1;
  background-color: #f1f1f1;
  padding: 20px;
  border-radius: 5px;
  margin-right: 10px;
}

.growth-chart {
  max-width: 100%;
  height: auto;
  flex: 1;
  background-color: #f1f1f1;
  padding: 20px;
  border-radius: 5px;
  margin-left: 10px;
}

/* #app {
  background-color: #FAF9F6;
  min-height: 100vh;
} */


</style>

<script>


export default {


  // extends: Pie,
  // props: ['data', 'options'],
  // mounted () {
  //   this.renderChart(this.data, this.options)
  // },

  data() {
    return {
      topTheatreRevenue: '',
      totalBookings: '',
      totalRevenue: '',
      topTheatreBookings: '',
      revenuePerTheatreChartLink: '',
      revenuePerMonthChartLink: '',

      response_message: '',
      
    };
  },
  async created() {
    try {
      const response = await fetch('http://localhost:5000/api/admin-home-page-stats', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      } else {
        const data = await response.json();
        this.topTheatreRevenue = data.topTheatreRevenue.theatre_name;
        this.totalBookings = data.totalBookings;
        this.totalRevenue = data.totalRevenue;
        this.topTheatreBookings = data.topTheatreBookings.theatre_name;
        this.revenuePerTheatreChartLink = data.revenuePerTheatreChart;
        this.revenuePerMonthChartLink = data.revenuePerMonthChart;
      }
    } catch (error) {
      console.error('Fetch to API failed:', error);
    }
  },
  methods: {

    generatePDF() {
    let contentOnlyHTML = this.$refs.contentOnly.outerHTML;
    fetch('http://127.0.0.1:5000/api/generate_pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
            html: contentOnlyHTML,
            data: {
              topTheatreRevenue: this.topTheatreRevenue,
              totalBookings: this.totalBookings,
              totalRevenue: this.totalRevenue,
              topTheatreBookings: this.topTheatreBookings,
              revenuePerTheatreChartLink: this.revenuePerTheatreChartLink,
              revenuePerMonthChartLink: this.revenuePerMonthChartLink,
            }
        }),
    })
    .then(response => {
        console.log(response);
        this.response_message="Succesfully initiated PDF generation of your dashboard.Please check Your mail for the same";
        
    })
    .catch(error => {
        console.log(error);
    })
}
  

  }
};
</script>


