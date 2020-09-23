
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
            disk_format: "", 
            "X-Auth-Token": this.props.token, 
            format_list: ['ami', 'ari', 'aki', 'vhd', 'vhdx', 'vmdk', 'raw', 'qcow2', 'vdi', 'ploop', 'iso'], 
            language_list: [ 'C/C++', 'Java' ]
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
        const url = 'http://164.125.70.19:16384/api/image/create';
        const data = new FormData();
        data.append('file', this.uploadInput.files[0]);

        const request = {
            method: 'POST', 
            headers: {
                "X-Auth-Token": this.state["X-Auth-Token"],  
                "name": this.state.image_name, 
                "min_ram": this.state.min_ram, 
                "min_disk": this.state.min_disk, 
                "disk_format": this.state.disk_format
            }, 
            body: data
        };

        fetch(url, request).then((response) => {
            if (response.status <= 210) alert("Image has been updated");
            else {
                alert("Image updating has been canceled by some reasons");
            }
        });
        
    }

    handleFormSubmit(e) {
        e.preventDefault();
        this.createImage();
        this.setState({
            image_name: '', 
            min_ram: 0, 
            min_disk: 0, 
            constraint_size: -1, 
            open: false, 
            disk_format: ""
        });
    }
    
    handleClose() {
        this.setState({
            image_name: '', 
            min_ram: 0, 
            min_disk: 0, 
            constraint_size: -1, 
            open: false, 
            disk_format: ""
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
                        <form onSubmit={this.handleFormSubmit}>
                        <TextField label="image_name" type="text" name="image_name" style={{width:240}} value={this.state.image_name} onChange={this.handleValueChange} margin="normal"/><br/>
                        <TextField label="min_ram (MB)" type="number" name="min_ram" style={{width:240}} value={this.state.min_ram} onChange={this.handleValueChange} margin="normal"/><br/>
                        <TextField label="min_disk (GB)" type="number" name="min_disk" style={{width:240}} value={this.state.min_disk} error={this.state.min_disk<=this.state.constraint_size} onChange={this.handleValueChange} margin="normal"/><br/>
                        <TextField label="disk_format" type="text" select onChange={this.handleValueChange} style={{width:240}} required name="disk_format" SelectProps={{
                                MenuProps: {
                                  className: classes.menu,
                                }
                            }} value={this.state.disk_format} onChange={this.handleValueChange} margin="normal"> 
                            {this.state.format_list.map((lang) => (
                                <MenuItem key={lang} style={{width:240}} value={lang}>
                                {lang}
                                </MenuItem>
                            ))}
                        </TextField><br/><br/>
                        <input type="file" name="image_file" id="image_file" accept="*" ref={(ref) => { this.uploadInput = ref; }} value={this.state.file} onChange={this.handleValueChange} /><br/><br/>
                        </form>
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
