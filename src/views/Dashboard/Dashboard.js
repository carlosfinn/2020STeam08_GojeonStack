import React, { Component } from "react";
// react plugin for creating charts
import ChartistGraph from "react-chartist";
// @material-ui/core
import { makeStyles } from "@material-ui/core/styles";
import Icon from "@material-ui/core/Icon";
// @material-ui/icons
import Store from "@material-ui/icons/Store";
import Warning from "@material-ui/icons/Warning";
import DateRange from "@material-ui/icons/DateRange";
import LocalOffer from "@material-ui/icons/LocalOffer";
import Update from "@material-ui/icons/Update";
import ArrowUpward from "@material-ui/icons/ArrowUpward";
import AccessTime from "@material-ui/icons/AccessTime";
import Accessibility from "@material-ui/icons/Accessibility";
import BugReport from "@material-ui/icons/BugReport";
import Code from "@material-ui/icons/Code";
import Cloud from "@material-ui/icons/Cloud";
// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import Table from "components/Table/Table.js";
import Tasks from "components/Tasks/Tasks.js";
import CustomTabs from "components/CustomTabs/CustomTabs.js";
import Danger from "components/Typography/Danger.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardIcon from "components/Card/CardIcon.js";
import CardBody from "components/Card/CardBody.js";
import CardFooter from "components/Card/CardFooter.js";
import HeatApi from "components/Openstack.jsx";
import CreateStack from "components/Dialog/CreateStack.jsx";
import CreateThread from "components/Dialog/CreateThread.jsx";
import withStyles from "@material-ui/core/styles/withStyles";
import PostTable from "components/PostTable.jsx";
import PropTypes from "prop-types";

import { bugs, website, server } from "variables/general.js";

import {
  dailySalesChart,
  emailsSubscriptionChart,
  completedTasksChart
} from "variables/charts.js";

import styles from "assets/jss/material-dashboard-react/views/dashboardStyle.js";

const useStyles = makeStyles(styles);

class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
    this.state = {
      "X-Auth-Token": this.props.location.state.token, 
      tenant_id: this.props.location.state.tenant_id, 
      role: this.props.location.state.role, 
      student_id: this.props.location.state.student_id, 
      thread_list: []
    };

  }

  render() {
    let teacherCreateMenu;
    if (this.state.role != "Student") {
      teacherCreateMenu = <CreateStack token={this.state["X-Auth-Token"]} tenant_id={this.state.tenant_id} creator_id={this.state.student_id}/>;
    } else {
      teacherCreateMenu = null;
    }
    const { thread_list } = this.state;

    return (
      <div>
        {teacherCreateMenu}<br/>
        <HeatApi token={this.state["X-Auth-Token"]} tenant_id={this.state.tenant_id} 
        cardCategory={this.props.classes.cardCategory} 
        cardTitle={this.props.classes.cardTitle} role={this.state.role}
        stats={this.props.classes.stats} student_id={this.state.student_id}/>
        <GridContainer>
          <GridItem xs={12} sm={12} md={12}>
            <Card>
              <CardHeader color="primary">
                <h4 className={this.props.classes.cardTitleWhite}>과목 공지사항</h4>
                <p className={this.props.classes.cardCategoryWhite}>
                  과목 공지사항을 여기에다 올립니다. 
                </p>
              </CardHeader>
              <CardBody>
                <CreateThread tenant_id={this.state.tenant_id} token={this.state["X-Auth-Token"]} student_id={this.state.student_id} />
                <PostTable tenant_id={this.state.tenant_id} token={this.state["X-Auth-Token"]} student_id={this.state.student_id} role={this.state.role} />
              </CardBody>
            </Card>
          </GridItem>
        </GridContainer>
      </div>
    );
  }
}

Dashboard.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(Dashboard);