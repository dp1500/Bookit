
<template>
    <div class="wrapper">
    <!-- Sidebar  -->
    <nav id="sidebar">
        <div class="sidebar-header">
            <h3>BookIt</h3>
        </div>

        <ul class="list-unstyled components">
            <p>Dummy Heading</p>
            <li class="active">
                <a href="#homeSubmenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">Home</a>
                <ul class="collapse list-unstyled" id="homeSubmenu">
                    <li>
                        <a href="#">Home 1</a>
                    </li>
                    <li>
                        <a href="#">Home 2</a>
                    </li>
                    <li>
                        <a href="#">Home 3</a>
                    </li>
                </ul>
            </li>
            <li>
                <a href="#">About</a>
            </li>
            <li>
                <a href="#pageSubmenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">Pages</a>
                <ul class="collapse list-unstyled" id="pageSubmenu">
                    <li>
                        <a href="#">Page 1</a>
                    </li>
                    <li>
                        <a href="#">Page 2</a>
                    </li>
                    <li>
                        <a href="#">Page 3</a>
                    </li>
                </ul>
            </li>
            <li>
                <a href="#">Portfolio</a>
            </li>
            <li>
                <a href="#">Contact</a>
            </li>
        </ul>

        <ul class="list-unstyled CTAs">
            <li>
                <a href="https://bootstrapious.com/tutorial/files/sidebar.zip" class="download">Download source</a>
            </li>
            <li>
                <a href="https://bootstrapious.com/p/bootstrap-sidebar" class="article">Back to article</a>
            </li>
        </ul>
    </nav>

    <!-- Page Content  -->
    <div id="content">

        
      <div class="dashboard">
        <div class="statistics">
          <div class="statistic-item">
            <div class="statistic-item-inner">
              <h4>Top Theatre (Revenue)</h4>
              <p>{{ topTheatre }}</p>
            </div>
          </div>
          <div class="statistic-item">
            <div class="statistic-item-inner">
              <h4>Total Bookings</h4>
              <p>{{ totalBookings }}</p>
            </div>
          </div>
          <div class="statistic-item">
            <div class="statistic-item-inner">
              <h4>Total Revenue</h4>
              <p>{{ totalRevenue }}</p>
            </div>
          </div>
          <div class="statistic-item">
            <div class="statistic-item-inner">
              <h4>Another Statistic</h4>
              <p>{{ anotherStatistic }}</p>
            </div>
          </div>
        </div>

        <div class="charts">
          <div class="growth-chart">
            <!-- Add your growth chart here -->
          </div>
          <div class="revenue-chart">
            <!-- Add your revenue pie chart here -->
          </div>
        </div>
      </div>
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

  .charts {
    display: flex;
    justify-content: space-between;
    height: 100%;
  }

  .growth-chart {
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
  }
</style>

<script>
export default {
  data() {
    return {
      topTheatre: 'Top Theatre Name',
      totalBookings: 100,
      totalRevenue: '$10,000',
      anotherStatistic: 'Another Statistic Value',
    };
  },
};
</script>