import React from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import Table from "components/Table/Table.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardBody from "components/Card/CardBody.js";
import PropTypes from "prop-types";
import withStyles from "@material-ui/core/styles/withStyles";
import Button from '@material-ui/core/Button';
import CreateImage from "components/Dialog/CreateImage.jsx";

const styles = {
  cardCategoryWhite: {
    "&,& a,& a:hover,& a:focus": {
      color: "rgba(255,255,255,.62)",
      margin: "0",
      fontSize: "14px",
      marginTop: "0",
      marginBottom: "0"
    },
    "& a,& a:hover,& a:focus": {
      color: "#FFFFFF"
    }
  },
  cardTitleWhite: {
    color: "#FFFFFF",
    marginTop: "0px",
    minHeight: "auto",
    fontWeight: "300",
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    marginBottom: "3px",
    textDecoration: "none",
    "& small": {
      color: "#777",
      fontSize: "65%",
      fontWeight: "400",
      lineHeight: "1"
    }
  }
};

const useStyles = makeStyles(styles);

class TableList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      "X-Auth-Token": "gAAAAABfV3JHy-vZJbfIfN5xbNgO5zuTcRkvwsMse5-PnWR6RYBtLBgPkZmkEriNNZBry9n_7kMvN3nWL8xAQSOR2Ps5i0EO5N1jxA73-0N7hodXfRwklBIMyxsRurWOxyCdxNTDketNE0U3m90084iLOFbAtYE4oSIrkAFl1jYrVHyooBXH1NM", 
      token: null,
      tenant_id: "c6d6b85938224e3ba6879d07e77fb4ce", 
      role: "Teacher", 
      student_id: "Baldi", 
      images: []
    }
    this.updateInfo();
    this.interval = setInterval(() => {
      this.updateInfo();
    },5000);
  }

  getImageInfo = async() => {
    fetch("http://164.125.70.19:16384/api/image/table", {
      headers: {
        "X-Auth-Token": this.state["X-Auth-Token"]
      }
    }).then((res) => res.json()).then((json) => this.setState({
      images: json
    }))
  }

  updateInfo = async() => {
    try {
      this.getImageInfo();
    } catch (error) {
      console.log(error);
    }
  }
  
  render() {
    var test = this.state.images;

    let teacherImageMenu = <CreateImage token={this.state["X-Auth-Token"]} tenant_id={this.state.tenant_id}/>;

    for (var i=0; i<test.length; i++) {
      console.log()
      const id = test[i][5];
      const token = this.state['X-Auth-Token'];

      let deletebutton = <Button variant="contained" color="primary" onClick={function(event) {
        event.preventDefault();

        const url = "http://164.125.70.19:16384/api/image/delete";

        const request = {
            method: 'DELETE', 
            headers: {
                "X-Auth-Token": token, 
                "image_id": id
            }
        };
        console.log(request);

        fetch(url, request).then((response) => {
          if (response.status <= 210) alert("Image has been deleted successfully");
          else {
              alert("The error occured by some reasons");
          }
      });;
      }}>DELETE</Button>;
      test[i][6] = deletebutton;
    }

    return (
      <GridContainer>
        <GridItem xs={12} sm={12} md={12}>
          {teacherImageMenu}
          <Card>
            <CardHeader color="primary">
              <h4 className={this.props.classes.cardTitleWhite}>Image list</h4>
              <p className={this.props.classes.cardCategoryWhite}>
                Here is a list of images for virtual machiene
              </p>
            </CardHeader>
            <CardBody>
              <Table
                tableHeaderColor="primary"
                tableHead={["Name", "Minimun RAM (MB)", "Minimum Disk (GB)", "Disk Format", "Status", "Image_id", "Delete"]}
                tableData={this.state.images}
              />
            </CardBody>
          </Card>
        </GridItem>
      </GridContainer>
    );
  }
}

TableList.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(TableList);
