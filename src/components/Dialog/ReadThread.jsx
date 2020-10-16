
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
//import fileDownload from 'js-file-download';

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
            date: this.props.written, 
            content: '',
            "X-Auth-Token": this.props.token, 
            deletable: this.props.deletable, 
            file_url: ''
        }

        this.handleFormSubmit = this.handleFormSubmit.bind(this);
        this.handleValueChange = this.handleValueChange.bind(this);
        this.handleClickOpen = this.handleClickOpen.bind(this);
        this.handleClose = this.handleClose.bind(this);
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
    
    handleValueChange(e) {
        e.preventDefault();
        let nextState = {};
        nextState[e.target.name] = e.target.value;
        this.setState(nextState);
        console.log(nextState);
    }

    deletePost() {
        const url = 'http://164.125.70.19:16384/api/board/delete';

        const request = {
            method: 'DELETE', 
            headers: {
                "X-Auth-Token": this.state["X-Auth-Token"], 
                foldername: this.state.foldername, 
                student_id: this.state.student_id, 
                tenant_id: this.state.tenant_id, 
                post_id: this.state.thread_id
            }
        }

        fetch(url, request).then((response) => {
            if (response.ok) alert("Deleted successfully");
            else alert("Deletion Error");
        })
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
        var url = 'http://164.125.70.19:16384/api/board/file?token=' + this.state["X-Auth-Token"] + 
            '&foldername=' + this.state.foldername + '&student_id=' + this.state.student_id + '&tenant_id=' + this.state.tenant_id + '&filename=' + this.state.filename;
        let deleteButton;

        if (this.state.deletable) deleteButton = <Button variant="contained" color="primary" onClick={this.handleFormSubmit}>Delete</Button>;
        else deleteButton = null;

        return (
            <TableRow className={classes.tableBodyRow}>
                <TableCell className={classes.tableCell}>
                    {this.state.thread_id}
                </TableCell>
                <TableCell className={classes.tableCell}>
                    <a onClick={this.handleClickOpen}>{this.state.title}</a>
                    <Dialog open={this.state.open} onClose={this.handleClose}>
                        <DialogTitle>Read posts</DialogTitle>
                            <DialogContent>
                                <TextField label="title" type="text" name="title" style={{width:500}} InputProps={{readOnly: true}} value={this.state.title} error={!this.state.title} onChange={this.handleValueChange} margin="normal"/><br/>
                                <TextField label="content" type="number" name="content" style={{width:500}} InputProps={{readOnly: true}} rows={10} multiline value={this.state.content} error={!this.state.title} onChange={this.handleValueChange} margin="normal"/><br/>
                                <a href={url} download={this.state.filename}>{this.state.filename}</a>
                            </DialogContent>
                        <DialogActions>
                            {deleteButton}
                            <Button variant="outlined" color="primary" onClick={this.handleClose}>Close</Button>
                        </DialogActions>
                    </Dialog>
                </TableCell>
                <TableCell className={classes.tableCell}>
                    {this.state.student_id}
                </TableCell>
                <TableCell className={classes.tableCell}>
                    {this.state.date}
                </TableCell>
            </TableRow>
        );
        //onClick={this.downloadFile}
        //href={this.state.file_url} 
    }
}    
export default withStyles(styles)(ReadThread);
