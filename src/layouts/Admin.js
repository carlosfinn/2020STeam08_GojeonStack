import React from "react";
import PropTypes from "prop-types";
import { Switch, Route, Redirect } from "react-router-dom";
// creates a beautiful scrollbar
import PerfectScrollbar from "perfect-scrollbar";
import "perfect-scrollbar/css/perfect-scrollbar.css";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import withStyles from "@material-ui/core/styles/withStyles";
// core components
import Navbar from "components/Navbars/Navbar.js";
import Footer from "components/Footer/Footer.js";
import Sidebar from "components/Sidebar/Sidebar.js";

import RegisterPage from "views/Auth/RegisterPage";

import routes from "routes.js";

import styles from "assets/jss/material-dashboard-react/layouts/adminStyle.js";

import image from "assets/img/sidebar-5.jpg";
import logo from "assets/img/icon4.png";

let ps;

class Dashboard extends React.Component {

  state = {
    image: image,
    color: "blue",
    hasImage: true,
    fixedClasses: "dropdown show",
    mobileOpen: false,
    token: null,
    tenant_id: null,
    student_id: null,
    user_id: null,
    role: null
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

  getAuthRoute() {
    return window.location.pathname === "/admin/login" || window.location.pathname === "/admin/register";
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
    var switchRoutes;

    {
      this.props.location.state
        ? (switchRoutes = (
          <Switch>
            {routes.map((prop, key) => {
              if (prop.layout === "/admin") {
                return (
                  <Route
                    path={prop.layout + prop.path}
                    component={prop.component}
                    key={key}
                    // token={this.props.location.state.token}
                    // tenant_id={this.props.location.state.tenant_id}
                    // student_id={this.props.location.state.student_id}
                    // role={this.props.location.state.role}
                  />
                );
              }
              return null;
            })}

            <Route path="/admin/register" component={RegisterPage} />
            <Redirect from="/admin" to="/admin/login" />
          </Switch>
        )) : (
          switchRoutes = (
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
              <Route path="/admin/register" component={RegisterPage} />
              <Redirect from="/admin" to="/admin/login" />
            </Switch>
          )
        )
    }



    //console.log("Admin");
    const { classes, ...rest } = this.props;
    console.log(this.props)
    return (
      <div className={classes.wrapper}>

        {this.props.location.state ?
          <Sidebar
            routes={routes}
            logoText={"코딩 교육 시스템"}
            logo={logo}
            image={this.state.image}
            handleDrawerToggle={this.handleDrawerToggle}
            open={this.state.mobileOpen}
            color={this.state.color}
            token={this.props.location.state.token}
            tenant_id={this.props.location.state.tenant_id}
            student_id={this.props.location.state.student_id}
            user_id={this.props.location.state.user_id}
            role={this.props.location.state.role}
            {...rest} />
          : null
        }
        
        {this.getAuthRoute() ?
          (
            <div className={classes.authPanel} ref={this.mainPanel}>
              <Navbar
                routes={routes}
                handleDrawerToggle={this.handleDrawerToggle}
                {...rest}
              />
              <div className={classes.content}>
                <div className={classes.container}>{switchRoutes}</div>
              </div>
              <Footer />
            </div>
          ) : (
            <div className={classes.mainPanel} ref={this.mainPanel}>
              <Navbar
                routes={routes}
                handleDrawerToggle={this.handleDrawerToggle}
                {...rest}
              />
              <div className={classes.content}>
                <div className={classes.container}>{switchRoutes}</div>
              </div>
              <Footer />
            </div>
          )
        }

        
      </div>
    );
  }
}

Dashboard.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(Dashboard);
