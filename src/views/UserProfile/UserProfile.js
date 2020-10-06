import React, { Component } from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import withStyles from "@material-ui/core/styles/withStyles";
import InputLabel from "@material-ui/core/InputLabel";
// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import CustomInput from "components/CustomInput/CustomInput.js";
import Button from "components/CustomButtons/Button.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardAvatar from "components/Card/CardAvatar.js";
import CardBody from "components/Card/CardBody.js";
import CardFooter from "components/Card/CardFooter.js";

import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import TextField from '@material-ui/core/TextField';


import studentAvatar from "assets/img/faces/student.png";
import teacherAvatar from "assets/img/faces/teacher.png";

const styles = {
  cardCategoryWhite: {
    color: "rgba(255,255,255,.62)",
    margin: "0",
    fontSize: "14px",
    marginTop: "0",
    marginBottom: "0"
  },
  cardTitleWhite: {
    color: "#FFFFFF",
    marginTop: "0px",
    minHeight: "auto",
    fontWeight: "300",
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    marginBottom: "3px",
    textDecoration: "none"
  }
};

//const useStyles = makeStyles(styles);



class UserProfile extends Component {
  constructor(props) {
    super(props);

    this.state = {
      token: this.props.location.state.token,
      tenant_id: this.props.location.state.tenant_id,
      role: this.props.location.state.role, //Student,Teacher
      student_id: this.props.location.state.student_id, //id
      pw: '',
      new_pw: '',
      user_id: this.props.location.state.user_id,
      open: false
    }
    console.log(this.props);



  }
  handleClick = e => {
    this.setState({
      open: true
    });
  }

  handleChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value
    });
  }

  handleSubmit = e => {
    e.preventDefault();
    let pwInfo = {
      pw: this.state.pw,
      newPW: this.state.new_pw,
      user_id: this.state.user_id
    };

    fetch("http://164.125.70.19:16384/auth/password", {
      method: 'POST',
      headers: {
        'X-Auth-Token': this.state.token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(pwInfo)
    })
      .then(response => response.json())
      .then(responseData => {
        console.log(responseData.passwordChanged);
        if (responseData.passwordChanged) {
          this.setState({
            pw: '',
            new_pw: '',
            open: false
          });
          alert("비밀번호 변경 완료: " + responseData.newPW)
        }
        else {
          alert("Password cannot be reused ")
        }

      });


  }

  handleClose = e => {
    this.setState({
      pw: '',
      new_pw: '',
      open: false,
    });
  }

  render() {
    const { classes } = this.props;
    return (
      <div>
        <GridContainer>
          <GridItem xs={12} sm={12} md={12}>
            <Card profile>
              <CardAvatar profile>
                <a href="#pablo" onClick={e => e.preventDefault()}>
                  {/* <img src={avatar} alt="..." /> */}
                  {this.state.role === "Student" && <img src={studentAvatar} alt="..." />}
                  {this.state.role === "Teacher" && <img src={teacherAvatar} alt="..." />}
                </a>
              </CardAvatar>
              <CardBody profile>
                <h6 className={classes.cardCategory}>{this.state.role}</h6>
                <h4 className={classes.cardTitle}>{this.state.student_id}</h4>
                {/* <p className={classes.description}>
                  Don{"'"}t be scared of the truth because we need to restart the
                  human foundation in truth And I love you like Kanye loves Kanye
                  I love Rick Owens’ bed design but the back is...
              </p> */}
                <Button color="primary" round onClick={this.handleClick}>
                  Change Password
              </Button>
                <Dialog open={this.state.open} onClose={this.handleClose}>
                  <DialogTitle>Change Password</DialogTitle>
                  <DialogContent>
                    <TextField label="password" type="password" name="pw" style={{ width: 300 }} value={this.state.pw} onChange={this.handleChange} margin="normal" /><br />
                    <TextField label="new password" type="password" name="new_pw" value={this.state.new_pw} style={{ width: 300 }} onChange={this.handleChange} margin="normal" /><br />
                  </DialogContent>
                  <DialogActions>
                    <Button variant="contained" color="primary" onClick={this.handleSubmit}>Change</Button>
                    <Button variant="outlined" color="primary" onClick={this.handleClose}>Close</Button>
                  </DialogActions>
                </Dialog>
              </CardBody>
            </Card>
          </GridItem>
          {/* <GridItem xs={12} sm={12} md={6}>
            <Card>
              <CardHeader color="primary">
                <h4 className={classes.cardTitleWhite}>Edit Profile</h4>
                <p className={classes.cardCategoryWhite}>Complete your profile</p>
              </CardHeader>
              <CardBody>
                <GridContainer>
                  <GridItem xs={12} sm={12} md={5}>
                    <CustomInput
                      labelText="Company (disabled)"
                      id="company-disabled"
                      formControlProps={{
                        fullWidth: true
                      }}
                      inputProps={{
                        disabled: true
                      }}
                    />
                  </GridItem>
                  <GridItem xs={12} sm={12} md={3}>
                    <CustomInput
                      labelText="Username"
                      id="username"
                      formControlProps={{
                        fullWidth: true
                      }}
                    />
                  </GridItem>
                  <GridItem xs={12} sm={12} md={4}>
                    <CustomInput
                      labelText="Email address"
                      id="email-address"
                      formControlProps={{
                        fullWidth: true
                      }}
                    />
                  </GridItem>
                </GridContainer>
                <GridContainer>
                  <GridItem xs={12} sm={12} md={6}>
                    <CustomInput
                      labelText="First Name"
                      id="first-name"
                      formControlProps={{
                        fullWidth: true
                      }}
                    />
                  </GridItem>
                  <GridItem xs={12} sm={12} md={6}>
                    <CustomInput
                      labelText="Last Name"
                      id="last-name"
                      formControlProps={{
                        fullWidth: true
                      }}
                    />
                  </GridItem>
                </GridContainer>
                <GridContainer>
                  <GridItem xs={12} sm={12} md={4}>
                    <CustomInput
                      labelText="City"
                      id="city"
                      formControlProps={{
                        fullWidth: true
                      }}
                    />
                  </GridItem>
                  <GridItem xs={12} sm={12} md={4}>
                    <CustomInput
                      labelText="Country"
                      id="country"
                      formControlProps={{
                        fullWidth: true
                      }}
                    />
                  </GridItem>
                  <GridItem xs={12} sm={12} md={4}>
                    <CustomInput
                      labelText="Postal Code"
                      id="postal-code"
                      formControlProps={{
                        fullWidth: true
                      }}
                    />
                  </GridItem>
                </GridContainer>
                <GridContainer>
                  <GridItem xs={12} sm={12} md={12}>
                    <InputLabel style={{ color: "#AAAAAA" }}>About me</InputLabel>
                    <CustomInput
                      labelText="Lamborghini Mercy, Your chick she so thirsty, I'm in that two seat Lambo."
                      id="about-me"
                      formControlProps={{
                        fullWidth: true
                      }}
                      inputProps={{
                        multiline: true,
                        rows: 5
                      }}
                    />
                  </GridItem>
                </GridContainer>
              </CardBody>
              <CardFooter>
                <Button color="primary">Update Profile</Button>
              </CardFooter>
            </Card>
          </GridItem> */}
        </GridContainer>
      </div>
    );
  }
}

export default withStyles(styles)(UserProfile);
// export default function UserProfile() {
//   const classes = useStyles();
//   return (
//     <div>
//       <GridContainer>
//         <GridItem xs={12} sm={12} md={6}>
//           <Card>
//             <CardHeader color="primary">
//               <h4 className={classes.cardTitleWhite}>Edit Profile</h4>
//               <p className={classes.cardCategoryWhite}>Complete your profile</p>
//             </CardHeader>
//             <CardBody>
//               <GridContainer>
//                 <GridItem xs={12} sm={12} md={5}>
//                   <CustomInput
//                     labelText="Company (disabled)"
//                     id="company-disabled"
//                     formControlProps={{
//                       fullWidth: true
//                     }}
//                     inputProps={{
//                       disabled: true
//                     }}
//                   />
//                 </GridItem>
//                 <GridItem xs={12} sm={12} md={3}>
//                   <CustomInput
//                     labelText="Username"
//                     id="username"
//                     formControlProps={{
//                       fullWidth: true
//                     }}
//                   />
//                 </GridItem>
//                 <GridItem xs={12} sm={12} md={4}>
//                   <CustomInput
//                     labelText="Email address"
//                     id="email-address"
//                     formControlProps={{
//                       fullWidth: true
//                     }}
//                   />
//                 </GridItem>
//               </GridContainer>
//               <GridContainer>
//                 <GridItem xs={12} sm={12} md={6}>
//                   <CustomInput
//                     labelText="First Name"
//                     id="first-name"
//                     formControlProps={{
//                       fullWidth: true
//                     }}
//                   />
//                 </GridItem>
//                 <GridItem xs={12} sm={12} md={6}>
//                   <CustomInput
//                     labelText="Last Name"
//                     id="last-name"
//                     formControlProps={{
//                       fullWidth: true
//                     }}
//                   />
//                 </GridItem>
//               </GridContainer>
//               <GridContainer>
//                 <GridItem xs={12} sm={12} md={4}>
//                   <CustomInput
//                     labelText="City"
//                     id="city"
//                     formControlProps={{
//                       fullWidth: true
//                     }}
//                   />
//                 </GridItem>
//                 <GridItem xs={12} sm={12} md={4}>
//                   <CustomInput
//                     labelText="Country"
//                     id="country"
//                     formControlProps={{
//                       fullWidth: true
//                     }}
//                   />
//                 </GridItem>
//                 <GridItem xs={12} sm={12} md={4}>
//                   <CustomInput
//                     labelText="Postal Code"
//                     id="postal-code"
//                     formControlProps={{
//                       fullWidth: true
//                     }}
//                   />
//                 </GridItem>
//               </GridContainer>
//               <GridContainer>
//                 <GridItem xs={12} sm={12} md={12}>
//                   <InputLabel style={{ color: "#AAAAAA" }}>About me</InputLabel>
//                   <CustomInput
//                     labelText="Lamborghini Mercy, Your chick she so thirsty, I'm in that two seat Lambo."
//                     id="about-me"
//                     formControlProps={{
//                       fullWidth: true
//                     }}
//                     inputProps={{
//                       multiline: true,
//                       rows: 5
//                     }}
//                   />
//                 </GridItem>
//               </GridContainer>
//             </CardBody>
//             <CardFooter>
//               <Button color="primary">Update Profile</Button>
//             </CardFooter>
//           </Card>
//         </GridItem>
//         <GridItem xs={12} sm={12} md={6}>
//           <Card profile>
//             <CardAvatar profile>
//               <a href="#pablo" onClick={e => e.preventDefault()}>
//                 <img src={avatar} alt="..." />
//               </a>
//             </CardAvatar>
//             <CardBody profile>
//               <h6 className={classes.cardCategory}>CEO / CO-FOUNDER</h6>
//               <h4 className={classes.cardTitle}>Alec Thompson</h4>
//               <p className={classes.description}>
//                 Don{"'"}t be scared of the truth because we need to restart the
//                 human foundation in truth And I love you like Kanye loves Kanye
//                 I love Rick Owens’ bed design but the back is...
//               </p>
//               <Button color="primary" round>
//                 Follow
//               </Button>
//             </CardBody>
//           </Card>
//         </GridItem>
//       </GridContainer>
//     </div>
//   );
// }
