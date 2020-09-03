// import React from "react";
// import { Switch, Route, Redirect } from "react-router-dom";
// // creates a beautiful scrollbar
// import PerfectScrollbar from "perfect-scrollbar";
// import "perfect-scrollbar/css/perfect-scrollbar.css";
// // @material-ui/core components
// import { makeStyles } from "@material-ui/core/styles";
// // core components
// import Navbar from "components/Navbars/Navbar.js";
// import Footer from "components/Footer/Footer.js";
// import Sidebar from "components/Sidebar/Sidebar.js";
// import FixedPlugin from "components/FixedPlugin/FixedPlugin.js";

// import routes from "routes.js";

// import styles from "assets/jss/material-dashboard-react/layouts/adminStyle.js";

// import bgImage from "assets/img/sidebar-2.jpg";
// import logo from "assets/img/reactlogo.png";

/*!

=========================================================
* Material Dashboard React - v1.7.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/material-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";
import PropTypes from "prop-types";
import { Switch, Route, Redirect } from "react-router-dom";
// creates a beautiful scrollbar
import PerfectScrollbar from "perfect-scrollbar";
import "perfect-scrollbar/css/perfect-scrollbar.css";
// @material-ui/core components
import withStyles from "@material-ui/core/styles/withStyles";
// core components
import Navbar from "components/Navbars/Navbar.jsx";
import Footer from "components/Footer/Footer.jsx";
import Sidebar from "components/Sidebar/Sidebar.jsx";
import FixedPlugin from "components/FixedPlugin/FixedPlugin.jsx";

import routes from "routes.js";

import dashboardStyle from "assets/jss/material-dashboard-react/layouts/dashboardStyle.jsx";

import image from "assets/img/sidebar-2.jpg";
import logo from "assets/img/reactlogo.png";

let ps;

class Dashboard extends React.Component {

  state = {
    image: image,
    color: "blue",
    hasImage: true,
    fixedClasses: "dropdown show",
    mobileOpen: false,
    token: null
  };
  mainPanel = React.createRef();
  handleImageClick = image => {
    this.setState({ image: image });
  };
  handleColorClick = color => {
    this.setState({ color: color });
  };
  handleFixedClick = () => {
    if (this.state.fixedClasses === "dropdown") {
      this.setState({ fixedClasses: "dropdown show" });
    } else {
      this.setState({ fixedClasses: "dropdown" });
    }
  };
  handleDrawerToggle = () => {
    this.setState({ mobileOpen: !this.state.mobileOpen });
  };
  getRoute() {
    return window.location.pathname !== "/admin/maps";
  }
  resizeFunction = () => {
    if (window.innerWidth >= 960) {
      this.setState({ mobileOpen: false });
    }
  };
  componentDidMount() {
    if (navigator.platform.indexOf("Win") > -1) {
      ps = new PerfectScrollbar(this.mainPanel.current);
    }
    window.addEventListener("resize", this.resizeFunction);
  }
  componentDidUpdate(e) {
    if (e.history.location.pathname !== e.location.pathname) {
      this.mainPanel.current.scrollTop = 0;
      if (this.state.mobileOpen) {
        this.setState({ mobileOpen: false });
      }
    }
  }
  componentWillUnmount() {
    if (navigator.platform.indexOf("Win") > -1) {
      ps.destroy();
    }
    window.removeEventListener("resize", this.resizeFunction);
  }
  render() {
    const switchRoutes = (
        <Switch>
          {routes.map((prop, key) => {
            if (prop.layout === "/admin") {
              return (
                <Route
                  path={prop.layout + prop.path}
                  component={prop.component}
                  key={key}
                />
              );
            }
            return null;
          })}
          <Redirect from="/admin" to="/admin/login" />
        </Switch>
      );

    //console.log("Admin");
    const { classes, ...rest } = this.props;
    console.log(this.props.location.state)

    return (
      <div className={classes.wrapper}>

        {this.props.location.state ?
          <Sidebar
            routes={routes}
            logoText={"Broker System"}
            logo={logo}
            image={this.state.image}
            handleDrawerToggle={this.handleDrawerToggle}
            open={this.state.mobileOpen}
            color={this.state.color}
            {...rest} />
          : null
        }

        <div className={classes.mainPanel} ref={this.mainPanel}>
          <Navbar
            routes={routes}
            handleDrawerToggle={this.handleDrawerToggle}
            {...rest}
          />
          {/* On the /maps route we want the map to be on full screen - this is not possible if the content and conatiner classes are present because they have some paddings which would make the map smaller */}
          {this.getRoute() ? (
            <div className={classes.content}>
              <div className={classes.container}>{switchRoutes}</div>
            </div>
          ) : (
              <div className={classes.map}>{switchRoutes}</div>
            )}
          {this.getRoute() ? <Footer /> : null}
        </div>
      </div>
    );
  }
}

Dashboard.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(dashboardStyle)(Dashboard);

// let ps;

// const switchRoutes = (
//   <Switch>
//     {routes.map((prop, key) => {
//       if (prop.layout === "/admin") {
//         return (
//           <Route
//             path={prop.layout + prop.path}
//             component={prop.component}
//             key={key}
//           />
//         );
//       }
//       return null;
//     })}
//     <Redirect from="/admin" to="/admin/login" />
//   </Switch>
// );

// const useStyles = makeStyles(styles);

// export default function Admin({ ...rest }) {
//   // styles
//   const classes = useStyles();
//   // ref to help us initialize PerfectScrollbar on windows devices
//   const mainPanel = React.createRef();
//   // states and functions
//   const [image, setImage] = React.useState(bgImage);
//   const [color, setColor] = React.useState("blue");
//   const [fixedClasses, setFixedClasses] = React.useState("dropdown show");
//   const [mobileOpen, setMobileOpen] = React.useState(false);
//   const handleImageClick = image => {
//     setImage(image);
//   };
//   const handleColorClick = color => {
//     setColor(color);
//   };
//   const handleFixedClick = () => {
//     if (fixedClasses === "dropdown") {
//       setFixedClasses("dropdown show");
//     } else {
//       setFixedClasses("dropdown");
//     }
//   };
//   const handleDrawerToggle = () => {
//     setMobileOpen(!mobileOpen);
//   };
//   const getRoute = () => {
//     return window.location.pathname !== "/admin/maps";
//   };
//   const resizeFunction = () => {
//     if (window.innerWidth >= 960) {
//       setMobileOpen(false);
//     }
//   };
//   // initialize and destroy the PerfectScrollbar plugin
//   React.useEffect(() => {
//     if (navigator.platform.indexOf("Win") > -1) {
//       ps = new PerfectScrollbar(mainPanel.current, {
//         suppressScrollX: true,
//         suppressScrollY: false
//       });
//       document.body.style.overflow = "hidden";
//     }
//     window.addEventListener("resize", resizeFunction);
//     // Specify how to clean up after this effect:
//     return function cleanup() {
//       if (navigator.platform.indexOf("Win") > -1) {
//         ps.destroy();
//       }
//       window.removeEventListener("resize", resizeFunction);
//     };
//   }, [mainPanel]);
//   return (
//     <div className={classes.wrapper}>
//       <Sidebar
//         routes={routes}
//         logoText={"Creative Tim"}
//         logo={logo}
//         image={image}
//         handleDrawerToggle={handleDrawerToggle}
//         open={mobileOpen}
//         color={color}
//         {...rest}
//       />
//       <div className={classes.mainPanel} ref={mainPanel}>
//       <Navbar
//           routes={routes}
//           handleDrawerToggle={handleDrawerToggle}
//           {...rest}
//         />
//         {/* On the /maps route we want the map to be on full screen - this is not possible if the content and conatiner classes are present because they have some paddings which would make the map smaller */}
//         {getRoute() ? (
//           <div className={classes.content}>
//             <div className={classes.container}>{switchRoutes}</div>
//           </div>
//         ) : (
//           <div className={classes.map}>{switchRoutes}</div>
//         )}
//         {getRoute() ? <Footer /> : null}
        
//       </div>
//     </div>
//   );
// }
