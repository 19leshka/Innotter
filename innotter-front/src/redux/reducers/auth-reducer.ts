import {authAPI} from '../../api/api';
import { AppDispatch } from '../store';
import {AuthAction, AuthActionTypes, AuthState, FormDataTypes, SetUserData, SetLoginError} from "../types/auth";

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

export const loginThunkCreator = (formData: FormDataTypes) => async (dispatch: AppDispatch) => {
    const response = await authAPI.login(formData.email, formData.password);
    if(response.data.resultCode === 200) {
        const {id, username, email, image} = response.data.user;
        const {accessToken} = response.data.access_token;
        dispatch(setUserDataActionCreator(id, username, email, image, accessToken, true));
    }
    else {

    }
}

export default authReducer;