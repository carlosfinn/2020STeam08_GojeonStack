import React, { Component } from 'react';
import styled from 'styled-components';
import { Router, Switch, Route, Link, Redirect } from 'react-router-dom';
import { createBrowserHistory } from "history";
import Button from '../../styles/Button';
import palette from '../../styles/palette';

import Admin from "layouts/Admin.js";
import Dashboard from "views/Dashboard/Dashboard.js";


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

const hist = createBrowserHistory();

class LoginForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            id: '',
            pw: '',
            token: null, 
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
        fetch("http://0.0.0.0:5000/login",{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userInfo)
        })
            .then(response => response.json())
            .then(responseData => {
                if(responseData.loginResult) {
                    this.setState({
                        token: responseData.token
                    });
                    console.log(this.state.token);
                }
                else {
                    //다시 로그인화면으로 
                }
        });
        
    }


    render() {
        if(this.state.token != null) {
            return (
                // <Redirect
                //     to={{
                //         pathname: "/admin/dashboard",
                //         state: {
                //             token: this.state.token
                //         }
                                
                //     }}
                // />
                <Router history={hist}>
                    <Switch>
                        <Route path="/admin" component={Admin} />
                        <Route path="/admin/dashboard" component={Dashboard} />
                        <Redirect 
                            to={{
                                pathname: "/admin/dashboard",
                                state: {
                                    token: this.state.token
                                }    
                            }}
                        />
                    </Switch>
                </Router>
                
              
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
// const LoginForm = () => {
//     const [form, setForm] = useState({
//         id: '',
//         pw: '',
//     });
//     const { id, pw } = form;
//     const [token, setToken] = useState('');
    
//     const onChange = e => {
//         const nextForm = {
//             ...form,
//             [e.target.name]: e.target.value
//         };
//         setForm(nextForm);
//     };

//     const onSubmit = e => {
//         e.preventDefault();
//         setForm({
//             id: this.state.id,
//             pw: this.state.pw
//         });

//         fetch("http://0.0.0.0:5000/login",{
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(form)
//         })
//             .then(response => response.json())
//             .then(responseData => {
//                 if(responseData.loginResult) {
//                     setToken(responseData.token);
//                 }
//                 else {
//                     //다시 로그인화면으로 
//                 }
//             });

//     }

//     if(token != null) {
//         return (
//             <Redirect
//                 to={{
//                     pathname: "/main",
//                     state: {

//                     }
                    
//                 }}
//             />
//         );
//     }
//     return (
//         <AuthFormBlock>
//             <h3>로그인</h3>
//             <form onSubmit={onSubmit}>
//                 <StyledInput onChange={onChange} value={id} autoComplete="username" name="username" placeholder="id" />
//                 <StyledInput onChange={onChange} value={pw} autoComplete="new-password" name="password" placeholder="pw" type="password" />
//                 <ButtonWithMarginTop fullWidth cyan>로그인</ButtonWithMarginTop>
//             </form>
//             <Footer>
//                 <Link to="/register">회원가입</Link>
//             </Footer>
//         </AuthFormBlock>
            
//     );
// };

//export default LoginForm;