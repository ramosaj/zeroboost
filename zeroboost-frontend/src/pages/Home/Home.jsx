import { useState } from 'react'
import './Home.scss'
import { Card, CardContent, TextField, Button} from '@mui/material';
import { useNavigate, Link } from 'react-router-dom';

function Home() {

    

    return (
     <div>
        <div className="mb-4 bg-primary-subtle rounded-3">
          <div className="container-fluid py-5">
            <h1 className="display-5 fw-bold"> Welcome! </h1>
            <p className ='fs-4'> See what your favorite pros are cooking.  </p>
            <p className='fs-5'> Has V1 Comm always gone for demos? Has OpTic retals gotten more mechy over time? </p>
            <p className="col-md-8 fs-5"> Select a professional Rocket League player from the list. </p>
          </div>
        </div>
        <div className= 'pro container-fluid'>
          <div className='container-fluid py-5'>
            <h5 className="display-5 fw-bold"> Available Pros </h5>
              <Link to='/steam/{id}/dashboard'> Retals </Link>
              
          </div>
         
        </div> 
      </div>
    )
  }
  
  export default Home
  