
import React from 'react'
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import MenuItem from '@material-ui/core/MenuItem';
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import fs from 'fs';

import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
    hidden: {
        display: 'none'
    }
});
    
class ReadThread extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            title: this.props.title, 
            content_fname: this.props.content, 
            //subject: this.props.subject, 
            thread_id: this.props.thread_id, 
            filename: this.props.filename, 
            foldername: this.props.foldername, 
            student_id: this.props.student_id, 
            tenant_id: this.props.tenant_id, 
            content: '',
            "X-Auth-Token": this.props.token
        }

        this.handleFormSubmit = this.handleFormSubmit.bind(this);
        this.handleValueChange = this.handleValueChange.bind(this);
        this.handleClickOpen = this.handleClickOpen.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.downloadFile = this.downloadFile.bind(this);
    }
    
    handleClickOpen() {
        this.fetchPost();
        this.setState({
            open: true
        });
    }

    fetchPost() {
        const url = 'http://164.125.70.19:16384/api/board/fetchpost';

        const request = {
            method: 'GET', 
            headers: {
                "X-Auth-Token": this.state["X-Auth-Token"], 
                foldername: this.state.foldername, 
                student_id: this.state.student_id, 
                tenant_id: this.state.tenant_id, 
                filename: this.state.content_fname
            }
        }

        fetch(url, request).then((response) => response.text()).then((data) => this.setState({
            content: data
        }))
    }

    downloadFile() {
        const url = 'http://164.125.70.19:16384/api/board/file';

        const request = {
            method: 'GET', 
            headers: {
                "X-Auth-Token": this.state["X-Auth-Token"], 
                foldername: this.state.foldername, 
                student_id: this.state.student_id, 
                tenant_id: this.state.tenant_id, 
                filename: this.state.filename,
                'Content-Type': 'application/octet-stream'
            }
        }

        console.log(this.state.filename)

        fetch(url, request).then((response) => response.blob()).then((blob) => {
            // 2. Create blob link to download
            const url = window.URL.createObjectURL(new Blob([blob]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', this.state.filename);

            // 3. Append to html page
            document.body.appendChild(link);

            // 4. Force download
            link.click();

            // 5. Clean up and remove the link
            link.parentNode.removeChild(link);
            this.setState({
                loading: false
            });
        }).catch((error) => {
            error.json().then((json) => {
                this.setState({
                    errors: json,
                    loading: false
                });
            })
        });;
    }
    
    handleValueChange(e) {
        e.preventDefault();
        let nextState = {};
        nextState[e.target.name] = e.target.value;
        this.setState(nextState);
        console.log(nextState);
    }

    deletePost() {
        const url = 'http://164.125.70.19:16384/api/board/delete';
    }

    handleFormSubmit(e) {
        this.deletePost();
        this.setState({
            content: "", 
            subject: "", 
            open: false
        });
    }
    
    handleClose() {
        this.setState({
            content: "", 
            subject: "", 
            open: false
        });
    }
    
    render() {
        const { classes } = this.props;
        return (
            <TableRow className={classes.tableBodyRow}>
                <TableCell className={classes.tableCell}>
                    {this.state.thread_id}
                </TableCell>
                <TableCell className={classes.tableCell}>
                    <a onClick={this.handleClickOpen}>{this.state.title}</a>
                    <Dialog open={this.state.open} onClose={this.handleClose}>
                        <DialogTitle>Create Image</DialogTitle>
                            <DialogContent>
                                <TextField label="title" type="text" name="title" style={{width:500}} InputProps={{readOnly: true}} value={this.state.title} error={!this.state.title} onChange={this.handleValueChange} margin="normal"/><br/>
                                <TextField label="content" type="number" name="content" style={{width:500}} InputProps={{readOnly: true}} rows={10} multiline value={this.state.content} error={!this.state.title} onChange={this.handleValueChange} margin="normal"/><br/>
                                <a onClick={this.downloadFile}>{this.state.filename}</a>
                            </DialogContent>
                        <DialogActions>
                        <Button variant="contained" color="primary" onClick={this.deletePost}>Delete</Button>
                        <Button variant="outlined" color="primary" onClick={this.handleClose}>Close</Button>
                        </DialogActions>
                    </Dialog>
                </TableCell>
                <TableCell className={classes.tableCell}>
                    {this.state.student_id}
                </TableCell>
            </TableRow>
        );
    }
}    
export default withStyles(styles)(ReadThread);
