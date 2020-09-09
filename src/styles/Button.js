import React from 'react';
import styled, { css } from 'styled-components';

import palette from '../styles/palette';

const StyledButton = styled.button`
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight:bold;
    padding: 0.25rem 1rem;
    color: white;
    outline: none;
    cursor: pointer;

    background: ${palette.gray[8]};
    &:hover {
        background: ${palette.gray[8]};
    }

    ${props =>
        props.fullWidth &&
        css`
            padding-top: 0.75rem;
            padding-bottom: 0.75rem;
            width: 100%;
            font-size: 1.125rem;
    
        `
    }

    ${props =>
        props.halfHeight &&
        css`
            height: 50%;
    
        `
    }

    ${props =>
        props.studentButton &&
        css`
            border-radius: 100px;
            width: 47%;
            font-weight: normal;
            float: left;
            padding-top: 0.75rem;
            padding-bottom: 0.75rem;
            margin-right: 1rem;
            font-size: 1.125rem;
            margin-bottom: 1rem;
            background: ${palette.gray[6]};
            
        `
    }
    ${props =>
        props.clickedStudentButton &&
        css`
            border-radius: 100px;
            width: 47%;
            font-weight: normal;
            float: left;
            padding-top: 0.75rem;
            padding-bottom: 0.75rem;
            margin-right: 1rem;
            font-size: 1.125rem;
            margin-bottom: 1rem;
            background: ${palette.gray[8]};
            
        `
    }

    ${props =>
        props.teacherButton &&
        css`
            border-radius: 100px;
            width: 47%;
            font-weight: normal;
            float: left;
            padding-top: 0.75rem;
            padding-bottom: 0.75rem;
            font-size: 1.125rem;
            background: ${palette.gray[6]};
    
        `
    }

${props =>
        props.clickedTeacherButton &&
        css`
            border-radius: 100px;
            width: 47%;
            font-weight: normal;
            float: left;
            padding-top: 0.75rem;
            padding-bottom: 0.75rem;
            font-size: 1.125rem;
            background: ${palette.gray[8]};
    
        `
    }

    ${props =>
        props.cyan &&
        css`
            background: ${palette.cyan[5]};
            &:hover {
                background: ${palette.cyan[4]};
                
            }
    
        `
    }

`;

const Button = props => <StyledButton {...props} />;



export default Button;