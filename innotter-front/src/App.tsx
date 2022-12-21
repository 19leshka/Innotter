import React from 'react'
import {BrowserRouter, Routes, Route ,useNavigate} from 'react-router-dom'
import {Provider} from 'react-redux'
import { useTypedSelector } from "./hooks/useTypedSelector"
import store from './redux/store'
import Login from './components/Login'
import Register from './components/Register'
import Header from './components/Header'

const App:React.FC = () => {
    const navigate = useNavigate();
    const isAuth = useTypedSelector(state => state.auth.isAuth);
    React.useEffect(() => {
        if(!isAuth) navigate(`/login`);
    }, [])

    return (
        <div className="wrapper">
            <Header/>
            <div className="content">
                <Routes>
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/register" element={<Register/>}/>
                </Routes>
            </div> 
        </div>
    );
}

const Innotter:React.FC = () => {
    return (
        <BrowserRouter> 
            <Provider store={store}>
                <App />
            </Provider>
        </BrowserRouter>
    )
}

export default Innotter;
