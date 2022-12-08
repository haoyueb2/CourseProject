import React from 'react';
import { NavLink } from 'react-router-dom';

/**
 * Navigation of the whole lists
 * @returns html of the response
 */
const Navigation = () => {
  return (
    <nav className='main-nav'>
      <ul>
        <li><NavLink to='/scrapy'>Scrapy Urls</NavLink></li>
        <li><NavLink to='/Visualize'>Best Reviews</NavLink></li>
        <li><NavLink to='/searchQuery'>Search Name</NavLink></li>
        <li><NavLink to='/delete'>Delete Items</NavLink></li>
        <li><NavLink to='/export'>Export Items</NavLink></li>
      </ul>
    </nav>
  );
}

export default Navigation;
