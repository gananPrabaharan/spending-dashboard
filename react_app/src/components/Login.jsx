import React, { useState } from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import { Alert } from "react-bootstrap"
import { useHistory } from "react-router-dom";
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
        backgroundColor: "#af0b1c",
    },
    form: {
        width: '100%', // Fix IE 11 issue.
        marginTop: theme.spacing(1),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
}));

const Login = () => {
    const classes = useStyles();
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();
    const [state, setState] = useState({
        email: "",
        password: ""
    });

    const history = useHistory();
    
    async function handleSubmit(e) {
        e.preventDefault()
    
        try {
          setError("");
          setLoading(true);
          await login(state.email, state.password);
          setLoading(false);
          history.push("/");
        } catch (err){
            setError("Failed to log in");
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
                    Sign in
                </Typography>
                {error && <Alert variant="danger">{error}</Alert>}
                <form className={classes.form} noValidate>
                    <TextField variant="outlined" margin="normal" fullWidth label="Email Address" autoFocus
                        onChange={(e) => { setState({ ...state, email: e.target.value }) }}
                        value={state.email} />
                    <TextField variant="outlined" margin="normal" fullWidth label="Password" type="password" autoComplete="current-password"
                        onChange={(e) => { setState({ ...state, password: e.target.value }) }}
                        value={state.password} />
                    <FormControlLabel
                        control={<Checkbox value="remember" color="primary" />}
                        label="Remember me"/>
                    <Button type="submit" fullWidth variant="contained" color="primary" className={classes.submit} onClick={handleSubmit}
                        disabled={loading || state.email.length===0 || state.password.length===0}>
                    Sign In
                    </Button>
                    <Grid container>
                        <Grid item xs>
                            <Link href="#" variant="body2">
                                Forgot password?
                            </Link>
                        </Grid>
                        <Grid item>
                            <Link href="signup" variant="body2">
                                {"Don't have an account? Sign Up"}
                            </Link>
                        </Grid>
                    </Grid>
                </form>
            </div>
        </Container>
  );
}

export default Login