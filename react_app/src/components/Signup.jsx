import React, { useState } from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import { Alert } from "react-bootstrap"
import { useHistory } from "react-router-dom"

import { useAuth } from "../contexts/AuthContext"

const useStyles = makeStyles((theme) => ({
    paper: {
        marginTop: theme.spacing(8),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    avatar: {
        margin: theme.spacing(1),
        backgroundColor: theme.palette.secondary.main,
    },
    form: {
        width: '100%', // Fix IE 11 issue.
        marginTop: theme.spacing(3),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
}));

const SignUp = () => {
    const classes = useStyles();
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const { signup } = useAuth();
    const [state, setState] = useState({
        email: "",
        password: "",
        confirmPassword: ""
    });
    const history = useHistory();

    async function handleSubmit(e) {
        e.preventDefault();

        if (state.password !== state.confirmPassword) {
            return setError("Passwords do not match")
        }

        try {
          setError("");
          setLoading(true);
          await signup(state.email, state.password);
          setLoading(false);
          history.push("/");
        } catch (err) {
            const acceptedCodes = ["auth/invalid-email", "auth/weak-password", "auth/email-already-in-use"];
            if (acceptedCodes.includes(err.code)){
                setError(err.message);
            } else {
                setError("Failed to create an account");
            }
            setLoading(false);
        }        
    }

    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <div className={classes.paper}>
                <Avatar className={classes.avatar}>
                    <LockOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    Sign up
                </Typography>
                {error && <Alert variant="danger">{error}</Alert>}
                <form className={classes.form}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <TextField variant="outlined" required fullWidth label="Email Address" autoFocus
                                onChange={(e) => { setState({ ...state, email: e.target.value }) }}
                                value={state.email} />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField variant="outlined" required fullWidth label="Password" type="password" 
                                onChange={(e) => { setState({ ...state, password: e.target.value }) }}
                                value={state.password} />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField variant="outlined" required fullWidth label="Confirm Password" type="password" 
                                onChange={(e) => { setState({ ...state, confirmPassword: e.target.value }) }}
                                value={state.confirmPassword} />
                        </Grid>
                    </Grid>
                    <Button type="submit" fullWidth variant="contained" color="primary" className={classes.submit} onClick={handleSubmit}
                        disabled={loading || state.email.length === 0 || state.password.length === 0 || state.confirmPassword.length === 0} >
                        Sign Up
                    </Button>
                    <Grid container justify="flex-end">
                        <Grid item>
                            <Link href="login" variant="body2">
                                Already have an account? Sign in
                            </Link>
                        </Grid>
                    </Grid>
                </form>
            </div>
        </Container>
    );
}

export default SignUp;