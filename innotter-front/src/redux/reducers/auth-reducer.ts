import {authAPI} from '../../api/api'
import { TypedDispatch } from '../store'
import {AuthAction, AuthActionTypes, AuthState, RegisterFormDataTypes, LoginFormDataTypes, SetUserData, SetLoginError} from "../types/auth"

const initialState: AuthState = {
    id: null,
    username: null,
    email: null,
    image: null,
    accessToken: null,
    error: null,
    isAuth: false
}

const authReducer = (state = initialState, action: AuthAction): AuthState => {
    switch (action.type) {
        case AuthActionTypes.SET_USER_DATA:
            return {
                ...state,
                ...action.payload
            }
        case AuthActionTypes.SET_LOGIN_ERROR:
            return {
                ...state,
                error: action.payload
            }
        default: 
            return state;
    }
}

export const setUserDataActionCreator: SetUserData = (id, username, email, image, accessToken, isAuth) => ({
    type: AuthActionTypes.SET_USER_DATA,
    payload: {
        id: id,
        username: username,
        email: email,
        image: image,
        accessToken: accessToken,
        isAuth: isAuth
    }
})

export const setLoginErrorActionCreator: SetLoginError = (error) => ({
    type: AuthActionTypes.SET_LOGIN_ERROR,
    payload: error
})

export const loginThunkCreator = (formData: LoginFormDataTypes | RegisterFormDataTypes) => async (dispatch: TypedDispatch) => {
    const response = await authAPI.login(formData.email, formData.password);
    if(response.status === 200) {
        const {id, username, email, image} = response.data.user;
        const accessToken = response.data.access_token;
        dispatch(setUserDataActionCreator(id, username, email, image, accessToken, true));
    }
    else if (response.status === 403){
        dispatch(setLoginErrorActionCreator(response.data.detail))
    }
}

export const registerThunkCreator = (formData: RegisterFormDataTypes) => async (dispatch: TypedDispatch) => {
    const response = await authAPI.register(formData.email, formData.username, formData.password);
    if(response.status === 201) {
        dispatch(loginThunkCreator(formData));
    }
    else if (response.status === 400){
        dispatch(setLoginErrorActionCreator(response.data.detail))
    }
}

export default authReducer;