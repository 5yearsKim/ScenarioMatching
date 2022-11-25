import React from 'react';
import 'Styles/Navbar.css';

export default function Navbar() {
  return (
    <div className='navbar'>
      <a href='/' className='logo'>LIM-DEMO</a>
      <div className='links'>
        <a href='/about'>ABOUT</a>
        <a href='/grading'>GRADING</a>
        <a href='/script'>SCRIPT</a>
      </div>
    </div>
  );
}