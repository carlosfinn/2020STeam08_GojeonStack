
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
    
class CreateStack extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            stack_name: '', 
            vcpus: 0, 
            ram: 0, 
            disk: 0, 
            cpu_error: false, 
            ram_error: false, 
            disk_error: false, 
            image: '', 
            image_list: [],
            image_constraints: {}, 
            open: false, 
            "X-Auth-Token": this.props.token, 
            tenant_id: this.props.tenant_id
        }

        this.handleFormSubmit = this.handleFormSubmit.bind(this);
        this.handleValueChange = this.handleValueChange.bind(this);
        this.handleClickOpen = this.handleClickOpen.bind(this);
        this.handleClose = this.handleClose.bind(this);

    }
    
    handleClickOpen() {
        this.getImageInfo();
        this.setState({
            open: true
        });
    }

    getImageInfo = async() => {
        await fetch("http://localhost:5000/api/image/list", {
            method: 'GET', 
            headers: {
                "X-Auth-Token": "gAAAAABfK64mNuoSqG-fLUqY2NXBqhALbHfYk-fLgRvMgQdh1jepcrIk44YZqbOEQb8Q_FUFZpUeaCaeo4SujJxI2FHD47FSLmHrEr4EU9fHeeZ9p4MvPZ3xtPYPqEgJ91E4Sxz6PS52JNNtKUulZXdY1cOJriBAL8yedDunofCxtvSdqL61arw"
            }
        }).then((res) => res.json()).then((json) => this.setState({
            image_list: json
        }))

        try {
            var images = {};
            for (var image of this.state.image_list) {
                images[image["name"]] = {
                    "min_ram": image["min_ram"], 
                    "min_disk": image["min_disk"]
                }
            }
            this.setState({
                image_constraints: images
            })
            console.log(this.state.image_constraints);
        } catch (error) {
            console.log(error);
        }
    }
    
    handleValueChange(e) {
        let nextState = {};

        if (e.target.name == "vcpus" || e.target.name == "ram" || e.target.name == "disk") nextState[e.target.name] = Number(e.target.value);
        else nextState[e.target.name] = e.target.value;

        let selected = "";
        if (e.target.name == "image") selected = e.target.value;
        else selected = this.state.image;

        nextState['cpu_error'] = (e.target.name == "vcpus" ? e.target.value: this.state.vcpus) < 1;
        nextState['ram_error'] = (e.target.name == "ram" ? e.target.value: this.state.ram) < (this.state.image_constraints[selected]? this.state.image_constraints[selected]['min_ram']: 0);
        nextState['disk_error'] = (e.target.name == "disk" ? e.target.value: this.state.disk) < (this.state.image_constraints[selected]? this.state.image_constraints[selected]['min_disk']: 0);

        console.log(nextState);
        this.setState(nextState);
    }

    createStack() {
        const url = 'http://localhost:5000/api/stack/create';
        const requestBody = {
            stack_name: this.state.stack_name, 
            vcpus: this.state.vcpus, 
            ram: this.state.ram, 
            disk: this.state.disk, 
            image: this.state.image
        }
        const request = {
            method: 'POST', 
            headers: {
                "X-Auth-Token": "gAAAAABfK64mNuoSqG-fLUqY2NXBqhALbHfYk-fLgRvMgQdh1jepcrIk44YZqbOEQb8Q_FUFZpUeaCaeo4SujJxI2FHD47FSLmHrEr4EU9fHeeZ9p4MvPZ3xtPYPqEgJ91E4Sxz6PS52JNNtKUulZXdY1cOJriBAL8yedDunofCxtvSdqL61arw", 
                "tenant_id": "ac09f439d0d941c39060b52864146c62"
            }, 
            body: JSON.stringify(requestBody)
        };
        console.log(requestBody);

        fetch(url, request)
    }

    handleFormSubmit(e) {
        e.preventDefault();
        if (!this.state.disk_error && !this.state.ram_error && !this.state.cpu_error && (this.state.image != "")) {
            this.createStack();
            this.setState({
                stack_name: '', 
                vcpus: 0, 
                ram: 0, 
                disk: 0, 
                cpu_error: false, 
                ram_error: false, 
                disk_error: false, 
                image: '', 
                image_list: [],
                image_constraints: {}, 
                open: false
            });
        } else alert("이미지에서 요구하는 디스크 혹은 RAM의 용량을 충족하지 않습니다.");
    }
    
    handleClose() {
        this.setState({
            stack_name: '', 
            vcpus: 0, 
            ram: 0, 
            disk: 0, 
            cpu_error: false, 
            ram_error: false, 
            disk_error: false, 
            image: '', 
            image_list: [],
            image_constraints: {}, 
            open: false
        });
    }
    
    render() {
        const { classes } = this.props;
        return (
            <div>
            <Button variant="contained" color="primary" onClick={this.handleClickOpen}>
                Create Instance
            </Button>
            <Dialog open={this.state.open} onClose={this.handleClose}>
                <DialogTitle>Create Instance</DialogTitle>
                    <DialogContent>
                        <TextField label="stack_name" type="text" name="stack_name" style={{width:240}} value={this.state.stack_name} onChange={this.handleValueChange} margin="normal"/><br/>
                        <TextField label="vcpus" type="number" name="vcpus" value={this.state.vcpus} style={{width:240}} required error={this.state.cpu_error && (this.state.image != "")} onChange={this.handleValueChange} margin="normal"/><br/>
                        <TextField label="ram (MB)" type="number" name="ram" value={this.state.ram} style={{width:240}} required error={this.state.ram_error} onChange={this.handleValueChange} margin="normal"/><br/>
                        <TextField label="disk (GB)" type="number" name="disk" value={this.state.disk} style={{width:240}} required error={this.state.disk_error} onChange={this.handleValueChange} margin="normal"/><br/>
                        <TextField label="image" type="text" select onChange={this.handleValueChange} style={{width:240}} required name="image" SelectProps={{
                                MenuProps: {
                                  className: classes.menu,
                                }
                            }} value={this.state.image} onChange={this.handleValueChange} margin="normal"> 
                            {this.state.image_list.map((image) => (
                                <MenuItem key={image.name} style={{width:240}} value={image.name}>
                                {image.name}
                                </MenuItem>
                            ))}
                        </TextField><br/>
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
export default withStyles(styles)(CreateStack);
