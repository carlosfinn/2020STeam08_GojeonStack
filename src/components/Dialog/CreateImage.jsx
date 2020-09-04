
import React from 'react'
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import MenuItem from '@material-ui/core/MenuItem';

import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
    hidden: {
        display: 'none'
    }
});
    
class CreateImage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            image_name: "", 
            min_ram: 0, 
            min_disk: 0, 
            constraint_size: -1, 
            open: false, 
            "X-Auth-Token": this.props.token
        }

        this.handleFormSubmit = this.handleFormSubmit.bind(this);
        this.handleValueChange = this.handleValueChange.bind(this);
        this.handleClickOpen = this.handleClickOpen.bind(this);
        this.handleClose = this.handleClose.bind(this);
    }
    
    handleClickOpen() {
        this.setState({
            open: true
        });
    }
    
    handleValueChange(e) {
        let nextState = {};
        if (e.target.name != "image_file") nextState[e.target.name] = e.target.value;
        else if (e.target.files[0]) {
            console.log(e.target.files[0].size);
            nextState["constraint_size"] = e.target.files[0].size / 1024.0 / 1024.0 / 1024.0;
        } else nextState["constraint_size"] = -1;
        this.setState(nextState);
        console.log(nextState);
    }

    createImage() {
        const url = 'http://0.0.0.0:5000/api/image/create';
        const test = this.state;

        var reader = new FileReader();
        if (document.getElementById("image_file")) reader.readAsBinaryString(document.getElementById("image_file").files[0]);
        reader.onload = function(e) {
            const token = test["X-Auth-Token"];
            const request = {
                method: 'PUT', 
                headers: {
                    "X-Auth-Token": token,  
                    "name": test.image_name, 
                    "min_ram": test.min_ram, 
                    "min_disk": test.min_disk
                }, 
                body: reader.result
            };
    
            fetch(url, request).then((response) => {
                if (response.status <= 210) alert("Image has been updated");
                else {
                    alert("Image updating has been canceled by some reasons");
                }
            });
        }
    }

    handleFormSubmit(e) {
        e.preventDefault();
        this.createImage();
        this.setState({
            image_name: '', 
            min_ram: 0, 
            min_disk: 0, 
            constraint_size: -1, 
            open: false
        });
    }
    
    handleClose() {
        this.setState({
            image_name: '', 
            min_ram: 0, 
            min_disk: 0, 
            constraint_size: -1, 
            open: false
        });
    }
    
    render() {
        const { classes } = this.props;
        return (
            <div>
            <Button variant="contained" color="primary" onClick={this.handleClickOpen}>
                Create Image
            </Button>
            <Dialog open={this.state.open} onClose={this.handleClose}>
                <DialogTitle>Create Image</DialogTitle>
                    <DialogContent>
                        <TextField label="image_name" type="text" name="image_name" style={{width:240}} value={this.state.image_name} onChange={this.handleValueChange} margin="normal"/><br/>
                        <TextField label="min_ram (MB)" type="number" name="min_ram" style={{width:240}} value={this.state.min_ram} onChange={this.handleValueChange} margin="normal"/><br/>
                        <TextField label="min_disk (GB)" type="number" name="min_disk" style={{width:240}} value={this.state.min_disk} error={this.state.min_disk<=this.state.constraint_size} onChange={this.handleValueChange} margin="normal"/><br/><br/>
                        <input type="file" name="image_file" id="image_file" accept="*" value={this.state.file} onChange={this.handleValueChange} /><br/><br/>
                    </DialogContent>
                <DialogActions>
                <Button variant="contained" color="primary" onClick={this.handleFormSubmit}>OK</Button>
                <Button variant="outlined" color="primary" onClick={this.handleClose}>Close</Button>
                </DialogActions>
            </Dialog>
        </div>
        );
    }
}    
export default withStyles(styles)(CreateImage);
