
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
            title: "", 
            content: "", 
            subject: "", 
            open: false, 
            filename: "", 
            foldername: "", 
            tenant_id: this.props.tenant_id, 
            student_id: this.props.student_id, 
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

    async createPost() {
        const url = 'http://164.125.70.19:16384/api/board/thread';
        const data = new FormData();
        data.append('file', this.uploadInput.files[0]);

        const fileexists = this.uploadInput.files.length != 0;

        let upfilename = '';
        if (this.uploadInput.files[0]) upfilename = this.uploadInput.files[0].name

        const request = {
            method: 'POST', 
            headers: {
                "X-Auth-Token": this.state["X-Auth-Token"], 
                tenant_id: this.state.tenant_id, 
                student_id: this.state.student_id
            }, 
            body: JSON.stringify({
                filename: upfilename, 
                title: this.state.title, 
                content: this.state.content
            })
        };

        const Response = await fetch(url, request);
        const FileInfo = await Response.json();

        if (fileexists){    
            fetch('http://164.125.70.19:16384/api/board/file', {
                method: 'POST', 
                headers: {
                    "X-Auth-Token": this.state["X-Auth-Token"], 
                    tenant_id: this.state.tenant_id, 
                    student_id: this.state.student_id, 
                    filename: FileInfo.filename, 
                    foldername: FileInfo.foldername
                }, 
                body: data
            }).then((response) => {
                if (response.status <= 210) alert("The post was uploaded");
                else alert("Posting has been canceled by some reasons");
            });
        } else {
            if (Response.status <= 210) alert("The post was uploaded");
            else alert("Posting has been canceled by some reasons");
        }
        /*{
            if (response.status <= 210) alert("The post was uploaded");
            else {
                alert("Image updating has been canceled by some reasons");
            }
        } */
    }

    handleFormSubmit(e) {
        this.createPost();
        this.setState({
            title: "", 
            content: "", 
            subject: "", 
            filename: "", 
            foldername: "", 
            open: false
        });
    }
    
    handleClose() {
        this.setState({
            title: "", 
            content: "", 
            subject: "", 
            filename: "", 
            foldername: "", 
            open: false
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
                <DialogTitle>Write posts</DialogTitle>
                <form onSubmit={this.handleFormSubmit}>
                    <DialogContent>
                            <TextField label="title" type="text" name="title" style={{width:500}} value={this.state.title} error={!this.state.title} onChange={this.handleValueChange} margin="normal"/><br/>
                            <TextField label="content" type="text" name="content" style={{width:500}} multiline rows={10} value={this.state.content} error={!this.state.content} onChange={this.handleValueChange} margin="normal"/><br/><br/><br/>
                            <input type="file" name="file" id="file" accept="*" ref={(ref) => { this.uploadInput = ref; }} onChange={this.handleValueChange} />
                    </DialogContent>
                    <DialogActions>
                        <Button variant="contained" color="primary" onClick={this.handleFormSubmit}>OK</Button>
                        <Button variant="outlined" color="primary" onClick={this.handleClose}>Close</Button>
                    </DialogActions>
                </form>
            </Dialog>
        </div>
        );
        // type="submit" 
        // </form>
    }
}    
export default withStyles(styles)(CreateThread);
