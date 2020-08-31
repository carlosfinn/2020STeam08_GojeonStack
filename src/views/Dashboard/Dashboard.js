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
import CreateImage from "components/Dialog/CreateImage.jsx";
import withStyles from "@material-ui/core/styles/withStyles";
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
    this.state = {
      "X-Auth-Token": "gAAAAABfK64mNuoSqG-fLUqY2NXBqhALbHfYk-fLgRvMgQdh1jepcrIk44YZqbOEQb8Q_FUFZpUeaCaeo4SujJxI2FHD47FSLmHrEr4EU9fHeeZ9p4MvPZ3xtPYPqEgJ91E4Sxz6PS52JNNtKUulZXdY1cOJriBAL8yedDunofCxtvSdqL61arw", 
      tenant_id: "ac09f439d0d941c39060b52864146c62", 
      role: "Student", 
      student_id: "brronco"
    }
  }

  render() {
    let teacherCreateMenu;
    let teacherImageMenu;
    if (this.state.role != "Student") {
      teacherCreateMenu = <CreateStack token={this.state["X-Auth-Token"]} tenant_id={this.state.tenant_id}/>;
      teacherImageMenu = <CreateImage token={this.state["X-Auth-Token"]} tenant_id={this.state.tenant_id}/>;
    } else {
      teacherCreateMenu = null;
      teacherImageMenu = null;
    }
    return (
      <div>
        {teacherCreateMenu}<br/>
        {teacherImageMenu}<br/>
        <HeatApi token={this.state["X-Auth-Token"]} tenant_id={this.state.tenant_id} 
        cardCategory={this.props.classes.cardCategory} 
        cardTitle={this.props.classes.cardTitle} role={this.state.role}
        stats={this.props.classes.stats} student_id={this.state.student_id}/>
        <GridContainer>
          <GridItem xs={12} sm={12} md={4}>
            <Card chart>
              <CardHeader color="success">
                <ChartistGraph
                  className="ct-chart"
                  data={dailySalesChart.data}
                  type="Line"
                  options={dailySalesChart.options}
                  listener={dailySalesChart.animation}
                />
              </CardHeader>
              <CardBody>
                <h4 className={this.props.classes.cardTitle}>Daily Sales</h4>
                <p className={this.props.classes.cardCategory}>
                  <span className={this.props.classes.successText}>
                    <ArrowUpward className={this.props.classes.upArrowCardCategory} /> 55%
                  </span>{" "}
                  increase in today sales.
                </p>
              </CardBody>
              <CardFooter chart>
                <div className={this.props.classes.stats}>
                  <AccessTime /> updated 4 minutes ago
                </div>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card chart>
              <CardHeader color="warning">
                <ChartistGraph
                  className="ct-chart"
                  data={emailsSubscriptionChart.data}
                  type="Bar"
                  options={emailsSubscriptionChart.options}
                  responsiveOptions={emailsSubscriptionChart.responsiveOptions}
                  listener={emailsSubscriptionChart.animation}
                />
              </CardHeader>
              <CardBody>
                <h4 className={this.props.classes.cardTitle}>Email Subscriptions</h4>
                <p className={this.props.classes.cardCategory}>Last Campaign Performance</p>
              </CardBody>
              <CardFooter chart>
                <div className={this.props.classes.stats}>
                  <AccessTime /> campaign sent 2 days ago
                </div>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card chart>
              <CardHeader color="danger">
                <ChartistGraph
                  className="ct-chart"
                  data={completedTasksChart.data}
                  type="Line"
                  options={completedTasksChart.options}
                  listener={completedTasksChart.animation}
                />
              </CardHeader>
              <CardBody>
                <h4 className={this.props.classes.cardTitle}>Completed Tasks</h4>
                <p className={this.props.classes.cardCategory}>Last Campaign Performance</p>
              </CardBody>
              <CardFooter chart>
                <div className={this.props.classes.stats}>
                  <AccessTime /> campaign sent 2 days ago
                </div>
              </CardFooter>
            </Card>
          </GridItem>
        </GridContainer>
        <GridContainer>
          <GridItem xs={12} sm={12} md={6}>
            <CustomTabs
              title="Assignments:"
              headerColor="primary"
              tabs={[
                {
                  tabName: "Bugs",
                  tabIcon: BugReport,
                  tabContent: (
                    <Tasks
                      checkedIndexes={[0, 3]}
                      tasksIndexes={[0, 1, 2, 3]}
                      tasks={bugs}
                    />
                  )
                },
                {
                  tabName: "Website",
                  tabIcon: Code,
                  tabContent: (
                    <Tasks
                      checkedIndexes={[0]}
                      tasksIndexes={[0, 1]}
                      tasks={website}
                    />
                  )
                },
                {
                  tabName: "Server",
                  tabIcon: Cloud,
                  tabContent: (
                    <Tasks
                      checkedIndexes={[1]}
                      tasksIndexes={[0, 1, 2]}
                      tasks={server}
                    />
                  )
                }
              ]}
            />
          </GridItem>
          <GridItem xs={12} sm={12} md={6}>
            <Card>
              <CardHeader color="warning">
                <h4 className={this.props.classes.cardTitleWhite}>과목 공지사항</h4>
                <p className={this.props.classes.cardCategoryWhite}>
                  과목 공지사항을 여기에다 올립니다. 
                </p>
              </CardHeader>
              <CardBody>
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