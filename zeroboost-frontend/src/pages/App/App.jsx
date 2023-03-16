import { useState } from 'react'
import Home from '../../pages/Home/Home.jsx';
import { Card, CardContent, TextField, Button} from '@mui/material';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Dashboard  from '../../pages/Dashboard/Dashboard';



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/:platform/:id/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  
  )
}

export default App
