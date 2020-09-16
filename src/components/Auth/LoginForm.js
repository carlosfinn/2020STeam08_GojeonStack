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



class LoginForm extends Component {
    constructor(props) {
        super(props);
        
        this.state = {
            id: '',
            pw: '',
            token: null,
            tenant_id: null,
            student_id: null,
            user_id: null,
            role: null,
            loginresult: {}
        }
        
    }

    handleChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        });
    }

    handleSubmit = e => {
        e.preventDefault();
        let userInfo = {
            id: this.state.id,
            pw: this.state.pw
        };
        fetch("http://164.125.70.19:16384/auth/login",{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userInfo)
        }).then(response => {
            if (response.ok) return response.json();
            else {
                alert("회원정보 오류");
                return response.json();
            }
        }).then(responseData => {
            if(responseData.loginResult) {
                this.setState({
                    token: responseData.token,
                    tenant_id: responseData.tenant_id,
                    student_id: responseData.student_id,
                    user_id: responseData.user_id,
                    role: responseData.role
                });
                console.log(this.state.token);
            } else {
                //다시 로그인화면으로
                alert("ID와 비밀번호를 확인해주세요");
            }
        });
        
    }


    render() {
        if(this.state.token != null) {
            return (
                <Redirect
                    to={{
                        pathname: "/admin/dashboard",
                        state: {
                            token: this.state.token,
                            tenant_id: this.state.tenant_id,
                            student_id: this.state.student_id,
                            user_id: this.state.user_id,
                            role: this.state.role

                        }
                                
                    }}
                />
                
            );
        }
        return (
            <AuthFormBlock>
                <h3>로그인</h3>
                <form onSubmit={this.handleSubmit}>
                    <StyledInput onChange={this.handleChange} value={this.state.id} autoComplete="username" name="id" placeholder="ID" />
                    <StyledInput onChange={this.handleChange} value={this.state.pw} autoComplete="new-password" name="pw" placeholder="PW" type="password" />
                    <ButtonWithMarginTop fullWidth cyan>로그인</ButtonWithMarginTop>
                </form>
                <Footer>
                    <Link to="/admin/register">회원가입</Link>
                </Footer>
         </AuthFormBlock>
        );
    }
}

export default LoginForm;
