
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
    
class CreateThread extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            title: this.props.title, 
            content: this.props.content, 
            subject: this.props.subject, 
            thread_id: this.props.thread_id, 
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
        e.preventDefault();
        let nextState = {};
        nextState[e.target.name] = e.target.value;
        this.setState(nextState);
        console.log(nextState);
    }

    createPost() {
        const url = 'http://164.125.70.19:16384/api/board/create';
        const data = new FormData();
        data.append('file', this.uploadInput.files[0]);

        const request = {
            method: '', 
            headers: {
                "X-Auth-Token": this.state["X-Auth-Token"]
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
        this.createImage();
        this.setState({
            title: "", 
            content: "", 
            subject: ""
        });
    }
    
    handleClose() {
        this.setState({
            title: "", 
            content: "", 
            subject: ""
        });
    }
    
    render() {
        const { classes } = this.props;
        return (
            <div>
            <Button variant="contained" color="primary" onClick={this.handleClickOpen}>
                Write
            </Button>
            <Dialog open={this.state.open} onClose={this.handleClose}>
                <DialogTitle>Create Image</DialogTitle>
                    <DialogContent>
                        <form onSubmit={this.handleFormSubmit}>
                        <TextField label="Title" type="text" name="image_name" style={{width:600}} value={this.state.title} error={!this.state.title} onChange={this.handleValueChange} margin="normal"/><br/>
                        <TextField label="Content" type="number" name="min_ram" style={{width:600}} multiline value={this.state.Content} error={!this.state.title} onChange={this.handleValueChange} margin="normal"/><br/>
                        <input type="file" name="file" id="file" accept="*" ref={(ref) => { this.uploadInput = ref; }} value={this.state.file} onChange={this.handleValueChange} /><br/><br/>
                        </form>
                    </DialogContent>
                <DialogActions>
                <Button variant="contained" color="primary" onClick={this.createPost}>OK</Button>
                <Button variant="outlined" color="primary" onClick={this.handleClose}>Close</Button>
                </DialogActions>
            </Dialog>
        </div>
        );
    }
}    
export default withStyles(styles)(CreateThread);
