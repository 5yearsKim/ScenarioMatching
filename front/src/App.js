import React from 'react';
import Navbar from 'Components/Navbar';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';
import 'Styles/main.css';

import HomeScreen from 'Screens/HomeScreen';
import AboutScreen from 'Screens/AboutScreen';
import GradingScreen from 'Screens/GradingScreen';
import ScriptScreen from 'Screens/ScriptScreen';

export default function App() {
  return (
    <div className='root'>
      <Router>
        <Navbar/>
        <div className='under-nav'>
          <Routes>
            <Route exact path='/' element={<HomeScreen/>}/>
            <Route path='/about' element={<AboutScreen/>}/>
            <Route path='/grading' element={<GradingScreen/>}/>
            <Route path='/script' element={<ScriptScreen/>}/>
          </Routes>
        </div>


      </Router>
    </div>
  );
}