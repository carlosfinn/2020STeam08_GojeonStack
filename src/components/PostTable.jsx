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
import ReadThread from "components/Dialog/ReadThread.jsx";
import withStyles from "@material-ui/core/styles/withStyles";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import PropTypes from "prop-types";

import { bugs, website, server } from "variables/general.js";

import styles from "assets/jss/material-dashboard-react/components/tableStyle.js";

const useStyles = makeStyles(styles);

class PostTable extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
    this.state = {
      "X-Auth-Token": this.props.token, 
      tenant_id: this.props.tenant_id, 
      role: this.props.role, 
      student_id: this.props.student_id, 
      thread_list: []
    };
    this.fetchPosts();
    this.interval = setInterval(() => {
      this.fetchPosts();
    },20000);
  }

  fetchPosts() {
    fetch('http://164.125.70.19:16384/api/board/fetchall', {
      method: 'GET'
    }).then((response) => response.json()).then((json) => this.setState({
      thread_list: json
    }));
    console.log(this.state.thread_list);
  }

  render() {
    const { thread_list } = this.state;
    const { tableHead, tableData, tableHeaderColor } = this.props;

    return (
      <table className={this.props.classes.table}>
        <TableHead className={this.props.classes[tableHeaderColor + "TableHeader"]}>
          <TableRow className={this.props.classes.tableHeadRow}>
                <TableCell className={this.props.classes.tableCell + " " + this.props.classes.tableHeadCell} >
                  post_id
                </TableCell>
                <TableCell className={this.props.classes.tableCell + " " + this.props.classes.tableHeadCell} >
                  title
                </TableCell>
                <TableCell className={this.props.classes.tableCell + " " + this.props.classes.tableHeadCell} >
                  writer
                </TableCell>
                <TableCell className={this.props.classes.tableCell + " " + this.props.classes.tableHeadCell} >
                  uploaded_date
                </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {this.state.thread_list.map((thread) => {
            return (
              <ReadThread thread_id={thread.id} tenant_id={this.state.tenant_id} token={this.state["X-Auth-Token"]} student_id={thread.student_id}
              content={thread.content} filename={thread.filename} title={thread.title} foldername={thread.foldername} written={thread.written} deletable={(this.state.student_id == "admin")||(this.state.student_id == thread.student_id)} />
            );
          })}
        </TableBody>
      </table>
    );
  }
}

PostTable.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(PostTable);