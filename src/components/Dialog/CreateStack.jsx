
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
            personeel: 1, 
            cpu_error: false, 
            ram_error: false, 
            disk_error: false, 
            image: '', 
            image_list: [],
            image_constraints: {}, 
            open: false, 
            "X-Auth-Token": this.props.token, 
            tenant_id: this.props.tenant_id, 
            language: '', 
            language_list: ["C/C++", "Java"], 
            creator_id: this.props.creator_id
        }

        console.log(this.state);
        this.handleFormSubmit = this.handleFormSubmit.bind(this);
        this.handleValueChange = this.handleValueChange.bind(this);
        this.handleClickOpen = this.handleClickOpen.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.getImageInfo = this.getImageInfo.bind(this);
    }
    
    handleClickOpen() {
        this.interval = setInterval(() => {
            this.getImageInfo();
            this.checkConstraints();
        }, 1000);
        this.setState({
            open: true
        });
    }

    getImageInfo() {
        fetch("http://164.125.70.19:16384/api/image/list", {
            method: 'GET', 
            headers: {
                "X-Auth-Token": this.state["X-Auth-Token"]
            }
        }).then((res) => {
            if (res.status <= 210) return res.json();
            else {
                alert("List of images couldn`t be loaded.");
                this.handleClose();
                return {}
            }
        }).then((json) => this.setState({
            image_list: json
        }));
        this.checkConstraints();
    }

    checkConstraints() {
        var images = {};
        for (var image of this.state.image_list) {
            images[image["name"]] = {
                "min_ram": image["min_ram"], 
                "min_disk": image["min_disk"]
            }
        }
        console.log(images);
        this.setState({
            image_constraints: images
        });
    }
    
    handleValueChange(e) {
        let nextState = {};
        this.checkConstraints();

        if (e.target.name == "vcpus" || e.target.name == "ram" || e.target.name == "disk") nextState[e.target.name] = Number(e.target.value);
        else nextState[e.target.name] = e.target.value;

        let selected = "";
        if (e.target.name == "image") selected = e.target.value;
        else selected = this.state.image;

        nextState['cpu_error'] = (e.target.name == "vcpus" ? e.target.value: this.state.vcpus) < 1;
        nextState['ram_error'] = (e.target.name == "ram" ? e.target.value: this.state.ram) < (this.state.image_constraints[selected]? this.state.image_constraints[selected]['min_ram']: 0);
        nextState['disk_error'] = (e.target.name == "disk" ? e.target.value: this.state.disk) < (this.state.image_constraints[selected]? this.state.image_constraints[selected]['min_disk']: 0);

        this.setState(nextState);
    }

    createStack() {
        const url = 'http://164.125.70.19:16384/api/stack/create';
        const requestBody = {
            stack_name: this.state.stack_name, 
            vcpus: this.state.vcpus, 
            ram: this.state.ram, 
            disk: this.state.disk, 
            image: this.state.image, 
            personeel: this.state.personeel, 
            language: this.state.language, 
            creator_id: this.state.creator_id
        }
        const request = {
            method: 'POST', 
            headers: {
                "X-Auth-Token": this.state["X-Auth-Token"], 
                "tenant_id": this.state.tenant_id
            }, 
            body: JSON.stringify(requestBody)
        };
        console.log(requestBody);

        fetch(url, request)
    }

    handleFormSubmit(e) {
        e.preventDefault();
        if (!this.state.disk_error && !this.state.ram_error && !this.state.cpu_error && (this.state.image != "")) {
            if (this.state.personeel > 0) {
                this.createStack();
                this.setState({
                    stack_name: '', 
                    vcpus: 0, 
                    ram: 0, 
                    disk: 0, 
                    personeel: 1, 
                    cpu_error: false, 
                    ram_error: false, 
                    disk_error: false, 
                    image: '', 
                    image_list: [],
                    image_constraints: {}, 
                    open: false, 
                    language: ''
                });
            } else alert("수강자의 수는 반드시 한 명 이상으로 설정하십시오.");
        } else alert("이미지에서 요구하는 디스크 혹은 RAM의 용량을 충족하지 않습니다.");
    }
    
    handleClose() {
        this.setState({
            stack_name: '', 
            vcpus: 0, 
            ram: 0, 
            disk: 0, 
            personeel: 1, 
            cpu_error: false, 
            ram_error: false, 
            disk_error: false, 
            image: '', 
            image_list: [],
            image_constraints: {}, 
            open: false, 
            language: ''
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
                        <TextField label="personeel" type="number" name="personeel" value={this.state.personeel} style={{width:240}} required error={this.state.personeel<=0} onChange={this.handleValueChange} margin="normal"/><br/>
                        <TextField label="language" type="text" select onChange={this.handleValueChange} style={{width:240}} required name="language" SelectProps={{
                                MenuProps: {
                                  className: classes.menu,
                                }
                            }} value={this.state.language} onChange={this.handleValueChange} margin="normal"> 
                            {this.state.language_list.map((language) => (
                                <MenuItem key={language} style={{width:240}} value={language}>
                                {language}
                                </MenuItem>
                            ))}
                        </TextField><br/>
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
