import React, { Component } from 'react';
import styled from 'styled-components';
import { Link, Redirect } from 'react-router-dom';
import Button from '../../styles/Button';
import palette from '../../styles/palette';

const AuthFormBlock = styled.div`
    h3 {
        margin: 0;
        color: ${palette.gray[8]};
        margin-bottom: 1rem;
    }
`;

const StyledInput = styled.input`
    font-size: 1rem;
    border: none;
    border-bottom: 1px solid ${palette.gray[5]};
    padding-bottom: 0.5rem;
    outline: none;
    width: 100%;
    &:focus {
        color: $oc-teal-7;
        border-bottom: 1px solid ${palette.gray[7]}
    }
    & + & {
        margin-top: 1rem;
    }
`;



const Footer = styled.div`
    margin-top: 1rem;
    text-align: right;
    a {
        color: ${palette.gray[6]};
        text-decoration: underline;
        &:hover {
            color: ${palette.gray[9]};
        }
    }
`;

const ButtonWithMarginTop = styled(Button)`
    margin-top: 1rem;
`;

const ErrorMessage = styled.div`
    color: red;
    text-align: center;
    font-size: 0.875rem;
    margin-top: 1rem;

`;
const ConfirmMessage = styled.div`
    color: green;
    text-align: center;
    font-size: 0.875rem;
    margin-top: 1rem;

`;

class RegisterForm extends Component {

    state = {
        role: '',
        name: '',
        pw: '',
        pwConfirm: '',
        email: '',
        pwcheckErrorMessage: '',
        pwcheckError: '',
        userID: null,
        studentButtonStyle: true,
        teacherButtonStyle: true

    };

    handleStudentClick = (e) => {
        this.setState({
            role: "Student",
            studentButtonStyle: !this.state.studentButtonStyle,
            teacherButtonStyle: true
        });
        console.log(this.state.role);
    }

    handleTeacherClick = (e) => {
        this.setState({
            role: "Teacher",
            teacherButtonStyle: !this.state.teacherButtonStyle,
            studentButtonStyle: true
        });
        console.log(this.state.role);
    }

    handleChange = e => {
        this.setState({
            [e.target.name]: e.target.value
        });
    }

    handlePWChk = e => {
        this.setState({
            [e.target.name]: e.target.value
        });
        if(e.target.value !== this.state.pw) {
            this.setState({
                pwcheckErrorMessage: "비밀번호가 일치하지 않습니다",
                pwcheckError: "error"
            });
        }
        else if(e.target.value === this.state.pw) {
            this.setState({
                pwcheckErrorMessage: "비밀번호가 일치합니다",
                pwcheckError: "confirm"
            });
        }
        
    }

    handleSubmit = e => {
        e.preventDefault();
        let userInfo = {
            role: this.state.role,
            name: this.state.name,
            pw: this.state.pw,
            email: this.state.email
        };
        if(this.state.pwcheckError === "confirm") {
            fetch("http://164.125.70.19:16384/auth/register",{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userInfo)
            })
                .then(response => response.json())
                .then(responseData => {
                    if(responseData.registerResult) {
                        if(responseData.character === "Teacher") {
                            alert(this.state.role + '유저 회원가입 완료');
                            console.log(responseData.userID);
                            this.setState({
                                userID: responseData.userID
                            });
                
                        }
                        else if(responseData.character === "Student") {
                            alert(this.state.role + ' 유저 회원가입 완료');
                            console.log(responseData.userID)
                            this.setState({
                                userID: responseData.userID
                            });
                        }
                    
                    }
                    else {
                        alert("Conflicted user");
                        this.setState({
                            name: '',
                            pw: '',
                            pwConfirm: '',
                            email: ''
                        });
                    }
                });
        }
        else if(this.state.pwcheckError === "error") {
            alert("비밀번호를 다시 확인하세요");
        }
        
    }


    render() {
        if(this.state.userID != null) {
            return (
                <Redirect
                    to={{
                        pathname: "/admin/login",        
                    }}
                />
            );
        }
        return (
            <AuthFormBlock>
            <h3>회원가입</h3>
            <Button studentButton={this.state.studentButtonStyle} clickedStudentButton={!this.state.studentButtonStyle} value="student" onClick={this.handleStudentClick}>Student</Button>
            <Button teacherButton={this.state.teacherButtonStyle} clickedTeacherButton={!this.state.teacherButtonStyle} value="teacher" onClick={this.handleTeacherClick}>Teacher</Button>
            <form onSubmit={this.handleSubmit}>
                <StyledInput onChange={this.handleChange} autoComplete="username" name="name" value={this.state.name} placeholder="ID" />
                <StyledInput onChange={this.handleChange} autoComplete="new-password" name="pw" value={this.state.pw} placeholder="PW" type="password" />
                <StyledInput onChange={this.handlePWChk} autoComplete="new-password" name="pwConfirm" value={this.state.pwConfirm} placeholder="PW 확인" type="password" />
                <StyledInput name="email" placeholder="이메일" type="email" />
                {this.state.pwcheckError ==="error" && <ErrorMessage>{this.state.pwcheckErrorMessage}</ErrorMessage>}
                {this.state.pwcheckError ==="confirm" && <ConfirmMessage>{this.state.pwcheckErrorMessage}</ConfirmMessage>}
                <ButtonWithMarginTop fullWidth cyan>회원가입</ButtonWithMarginTop>
            </form>
            <Footer>
                <Link to="/admin/login">로그인</Link>
            </Footer>
        </AuthFormBlock>
        );
    }
}

export default RegisterForm;