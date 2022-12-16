import React from 'react';
import { Routes, Route } from 'react-router-dom';

import Search from './Search';
import Bookmarks from './Bookmarks';

const Main = () => {
  return (
    <Routes>
        {/* <Header/> */}
      <Route exact path='/' element={<Search/>}></Route>
      <Route exact path='/bookmarks' element={<Bookmarks/>}></Route>
    </Routes>
  );
} 

export default Main;