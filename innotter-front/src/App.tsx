import React from 'react'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import {Provider} from 'react-redux'
import store from './redux/store'
import Login from './components/Login'
import Register from './components/Register'

const App:React.FC = () => {
  return (
    <div>
      <Routes>
          <Route path="/login" element={<Login/>}/>
          <Route path="/register" element={<Register/>}/>
      </Routes>
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
