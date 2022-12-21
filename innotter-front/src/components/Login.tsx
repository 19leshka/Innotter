import { useState } from 'react'
import { useFormik, FormikErrors } from 'formik'
import { useAppDispatch } from '../hooks/useAppDispatch'
import {loginThunkCreator} from '../redux/reducers/auth-reducer'

import InputAdornment from '@mui/material/InputAdornment'
import IconButton from '@mui/material/IconButton'
import Visibility from '@mui/icons-material/Visibility'
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';



interface InitialValues {
    email: string,
    password: string
}

const validate = (values: InitialValues) => {


    let errors: FormikErrors<InitialValues> = {};

    if(!values.email) {
        errors.email = 'Required'
    }else if(!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(values.email))){
        errors.email = 'Invalid email'
    }

    if(!values.password) {
        errors.password = 'Required'
    }

    return errors;
}

const Login: React.FC = () => {
    const [showPassword, setShowPassword] = useState(false);
    const dispatch = useAppDispatch()

    const handleClickShowPassword = () => setShowPassword((show) => !show);

    const handleMouseDownPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();
    };

    const initialValues: InitialValues = {
        email: '',
        password: ''
    }

    const onSubmit = (values: InitialValues) => {
        let formData: InitialValues = {
            email: values.email,
            password: values.password
        }
        dispatch(loginThunkCreator(formData));
    }

    const formik = useFormik({
        initialValues,
        onSubmit,
        validate
    })

    return (
        <div className='form-container'>
            <form className='form' onSubmit={formik.handleSubmit}>
                <TextField
                    fullWidth
                    id="email"
                    name="email"
                    label="Email"
                    value={formik.values.email}
                    onChange={formik.handleChange}
                    error={formik.touched.email && Boolean(formik.errors.email)}
                    helperText={formik.touched.email && formik.errors.email}
                    sx={{
                        marginBottom: 2
                    }}
                />
                <TextField
                    fullWidth
                    id="password"
                    name="password"
                    label="Password"
                    type={showPassword ? 'text' : 'password'}
                    value={formik.values.password}
                    onChange={formik.handleChange}
                    error={formik.touched.password && Boolean(formik.errors.password)}
                    helperText={formik.touched.password && formik.errors.password}
                    InputProps={{
                        endAdornment: <InputAdornment position="end">
                                        <IconButton
                                        aria-label="toggle password visibility"
                                        onClick={handleClickShowPassword}
                                        onMouseDown={handleMouseDownPassword}
                                        >
                                        {showPassword ? <VisibilityOff /> : <Visibility />}
                                        </IconButton>
                                    </InputAdornment>
                    }}
                    sx={{
                        marginBottom: 2
                    }}
                />
                <Button color="primary" variant="contained" fullWidth type="submit">
                    Login
                </Button>
            </form>
        </div>
    )
}

export default Login