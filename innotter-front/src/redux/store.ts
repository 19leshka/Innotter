import {createStore, combineReducers, applyMiddleware} from 'redux'
import thunkMiddleware from 'redux-thunk'
import authReducer from './reducers/auth-reducer'


const rootReducer = combineReducers({
    auth: authReducer,
})

const store = createStore(rootReducer, applyMiddleware(thunkMiddleware))

export type RootState = ReturnType<typeof rootReducer>
export type AppDispatch = typeof store.dispatch


export default store