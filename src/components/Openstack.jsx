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
import { bugs, website, server } from "variables/general.js";
import Button from '@material-ui/core/Button';

class StackInfo extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      consoleData: {}, 
      "X-Auth-Token": this.props.token, 
      tenant_id: this.props.tenant_id, 
      role: this.props.role, 
      student_id: this.props.student_id, 
      stack_id: this.props.stack_id, 
      stack_name: this.props.stack_name, 
      owner: '', 
      enrolleddata: {}, 
      studentconsole: {}
    }
    
    if (this.state.role == "Student") {
      this.interval = setInterval(() => {
        this.checkEnrolled();
        if (this.state.enrolleddata.enrolled) this.enrollStudent();
      },10000);
    } else this.getConsoleLink();

    this.getOwner();
  }

  getOwner() {
    const check_url = "http://164.125.70.19:16384/api/stack/owner";
    fetch(check_url, {
      method: 'GET', 
      headers: {
        "stack_id": this.state.stack_id
      }
    }).then((res) => res.json()).then((json) => this.setState({
      owner: json.owner
    }));
  }

  getConsoleLink() {
    const url = "http://164.125.70.19:16384/api/stack/console";
    const request = {
      method: "POST", 
      headers: {
        "X-Auth-Token": this.state["X-Auth-Token"], 
        "tenant_id": this.state.tenant_id, 
        "stack_id": this.state.stack_id, 
        "stack_name": this.state.stack_name
      }
    }

    fetch(url, request).then((res) => res.json()).then((json) => this.setState({
      consoleData: json
    }))
  }

  checkEnrolled() {
    const check_url = "http://164.125.70.19:16384/api/stack/enrollcheck";
    fetch(check_url, {
      method: 'GET', 
      headers: {
        "stack_id": this.state.stack_id, 
        "student_id": this.state.student_id
      }
    }).then((res) => res.json()).then((json) => this.setState({
      enrolleddata: json
    }));
  }

  enrollStudent = () => {
    const url = "http://164.125.70.19:16384/api/stack/enrollconsole";

    const request = {
      method: "POST", 
      headers: {
        "X-Auth-Token": this.state["X-Auth-Token"], 
        "tenant_id": this.state.tenant_id, 
        "stack_id": this.props.stack_id, 
        "stack_name": this.props.stack_name, 
        "student_id": this.state.student_id
      }
    }

    this.checkEnrolled();
    console.log(this.state.enrolleddata);
    fetch(url, request).then((res) => {
      if (res.ok) return res.json();
      else alert("수강신청 등록 에러");
    }).then((json) => {
      this.setState({
        studentconsole: json
      });
    });
    console.log(this.state.studentconsole);
  }

  DeleteStack() {
    const url = "http://164.125.70.19:16384/api/stack/delete";
    console.log(this.state.stack_id);
    console.log(this.state.stack_name);

    const requestBody = {
      stack_name: this.state.stack_name, 
      stack_id: this.state.stack_id
    }
    const request = {
        method: 'DELETE', 
        headers: {
            "X-Auth-Token": this.state["X-Auth-Token"], 
            "tenant_id": this.state.tenant_id
        }, 
        body: JSON.stringify(requestBody)
    };

    fetch(url, request);
  }

  render() {
    const isStudent = this.state.role == "Student";
    let DeleteButton;
    let console;
    let LectureConsole;

    if (isStudent) {
      DeleteButton = <br/>;
      if (!this.state.enrolleddata.enrolled) LectureConsole = <Button variant="contained" color="primary" onClick={this.enrollStudent}>Take Lecture</Button>;
      else {
        LectureConsole = <a href={this.state.studentconsole.url}>Go to console</a>;
      }
    } else {
      if (this.state.student_id == this.state.owner) DeleteButton = <Button variant="contained" color="primary" onClick={this.DeleteStack.bind(this)}>DELETE</Button>;
      if (this.state.consoleData.url) LectureConsole = <a href={this.state.consoleData.url}>Go to console</a>;
      else LectureConsole = <a>The Lecture is still being creating</a>;
    }

    return (
      <GridContainer name={this.props.key}>
      <GridItem xs={12} sm={6} md={3}>
      <Card style={{height:150}}>
        <CardHeader color="warning" stats icon>
          <CardIcon color="warning">
            <Icon>content_copy</Icon>
          </CardIcon>
          <p className={this.props.cardCategory}>Stack name</p>
          <h3 className={this.props.cardTitle}>
            {this.props.stack_name}
          </h3>
        </CardHeader>
        <CardFooter>
          <div className={this.props.stats}>
            {DeleteButton}
          </div>
        </CardFooter>
      </Card>
    </GridItem>
    <GridItem xs={12} sm={6} md={3}>
      <Card style={{height:150}}>
        <CardHeader color="success" stats icon>
          <CardIcon color="success">
            <Store />
          </CardIcon>
          <p className={this.props.cardCategory}>Creation time</p>
          <h3 className={this.props.cardTitle}>{this.props.creation_time}</h3>
        </CardHeader>
        <CardFooter>
          <div className={this.props.stats}>
              <br></br>
          </div>
        </CardFooter>
      </Card>
    </GridItem>
    <GridItem xs={12} sm={6} md={3}>
      <Card style={{height:150}}>
        <CardHeader color="danger" stats icon>
          <CardIcon color="danger">
            <Icon>info_outline</Icon>
          </CardIcon>
          <p className={this.props.cardCategory}>Stack status</p>
          <h3 className={this.props.cardTitle}>{this.props.stack_status}</h3>
        </CardHeader>
        <CardFooter>
          <div className={this.props.stats}>
              <br></br>
          </div>
        </CardFooter>
      </Card>
    </GridItem>
    <GridItem xs={12} sm={6} md={3}>
      <Card style={{height:150}}>
        <CardHeader color="info" stats icon>
          <CardIcon color="info">
            <Accessibility />
          </CardIcon>
          <p className={this.props.cardCategory}>Owner (Instructor)</p>
          <h3 className={this.props.cardTitle}>{this.state.owner}</h3>
        </CardHeader>
        <CardFooter>
          <div className={this.props.stats}>
              {LectureConsole}
          </div>
        </CardFooter>
      </Card>
    </GridItem>
    </GridContainer>
    );
  }
}

export default class HeatApi extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [], 
      "X-Auth-Token": this.props.token, 
      tenant_id: this.props.tenant_id, 
      role: this.props.role, 
      student_id: this.props.student_id
    }
    this.updateInfo();
    this.interval = setInterval(() => {
      this.updateInfo();
    },20000);
  }

  getStackInfo = async() => {
    fetch("http://164.125.70.19:16384/api/stack/list", {
      headers: {
        "X-Auth-Token": this.state["X-Auth-Token"], 
        "tenant_id": this.state.tenant_id
      }
    }).then((res) => res.json()).then((json) => this.setState({
          data: json
    }))
  }

  updateInfo = async() => {
    try {
      this.getStackInfo();
    } catch (error) {
      console.log(error)
    }
  }

  render() {
    const { data } = this.state;
    return (
      <div>
        {this.state.data.map((stack, i) => {
          return (
              <StackInfo cardCategory={this.props.cardCategory} cardTitle={this.props.cardTitle} stats={this.props.stats}
              stack_name={stack.stack_name} creation_time={stack.creation_time} stack_status={stack.stack_status} stack_owner={stack.stack_owner}
              stack_id={stack.id} token={this.state["X-Auth-Token"]} tenant_id={this.state.tenant_id} role={this.state.role} student_id={this.state.student_id}
              />
          );
        })}
      </div>
    )
  }
}
