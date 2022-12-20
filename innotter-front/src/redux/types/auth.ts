export enum AuthActionTypes {
    SET_USER_DATA = 'SET_USER_DATA',
    SET_LOGIN_ERROR = 'SET_LOGIN_ERROR'
}


export interface AuthState {
    id: number | null,
    username: string | null,
    email: string | null,
    image: string | null,
    accessToken: string | null,
    error: string | null
    isAuth: boolean,
}

export interface FormDataTypes {
    email: string,
    password: string
}

interface SetUserDataAction {
    type: AuthActionTypes.SET_USER_DATA,
    payload: {
        id: null | number,
        email: null | string,
        username: null | string,
        accessToken: null | string,
        image: null | string
        isAuth: boolean,
    }
}

export type SetUserData = (id: number | null, username: string | null, email: string | null, image: string | null, accessToken: string | null, isAuth: boolean) => SetUserDataAction

interface SetLoginErrorAction {
    type: AuthActionTypes.SET_LOGIN_ERROR,
    payload: null | string
}

export type SetLoginError = (error: string | null) => SetLoginErrorAction


export type AuthAction = SetUserDataAction | SetLoginErrorAction