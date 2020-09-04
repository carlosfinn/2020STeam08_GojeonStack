/*!

=========================================================
* Material Dashboard React - v1.9.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2020 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/material-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";
import ReactDOM from "react-dom";
import { createBrowserHistory } from "history";
import { Router, Route, Switch, Redirect } from "react-router-dom";

// core components
import Admin from "layouts/Admin.js";
<<<<<<< HEAD
import RegisterPage from "views/Register/RegisterPage"
import LoginPage from "views/Login/LoginPage"
=======
>>>>>>> parent of 374042c... Auth 추가

import "assets/css/material-dashboard-react.css?v=1.9.0";
import Dashboard from "views/Dashboard/Dashboard";

const hist = createBrowserHistory();

//<Route path="/admin" component={Admin} />
//<Route path="/admin/register" component={RegisterPage}  />

ReactDOM.render(
  <Router history={hist}>
    <Switch>
<<<<<<< HEAD
      {/* <Route path="/admin" component={Admin} /> */}
      <Route path="/admin/login" component={LoginPage}  />
      <Route path="/admin/register" component={RegisterPage} />
      <Redirect from="/" to="/admin/login" />
=======
      <Route path="/admin" component={Admin} />
      <Redirect from="/" to="/admin/dashboard" />
>>>>>>> parent of 374042c... Auth 추가
    </Switch>
  </Router>,
  document.getElementById("root")
);
