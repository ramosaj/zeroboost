import { VictoryChart , VictoryScatter, VictoryLabel } from 'victory';
import {useState, useEffect, React } from 'react';
import { useParams } from 'react-router-dom';
import axios  from 'axios';
import './Dashboard.scss'



function Dashboard(props) {

    const [bpm, setBpm] = useState();
    const [shooting, setShooting] = useState();
    const { id, platform } = useParams();
    const [ ready , setReady] = useState(false);

    function transform_dates(data) { 
         data.forEach((element) => { 
                element['date'] = new Date(element['year'],element['month'])
         })

        
        return data
    }

    useEffect(() => { 
            console.log('hook triggered');
            axios.get(`http://localhost:3001/${platform}/${id}/`)
                .then(res => { 
                    console.log(res)
                    setReady(true)
                    setBpm(transform_dates(res['data']['bpm']))
                    setShooting(transform_dates(res['data']['shooting_percentage']))
                    
                });
            
    },[]);

    return ( 
        <div class='dashboard'> 
            <div class='row'>
                <div class='col'>
                { ready &&  <VictoryChart scale={{x: "time" }} className='bpm'>
                    <VictoryLabel x={200} y = {30} text="Boost Per Minute" />
                        <VictoryScatter 
                            data= { bpm }
                            x='date'
                            y='bpm'
                            domain={{y: [300,500]}}
                        />
                    </VictoryChart>
                }
                </div>

                <div class='col'> 
                {ready && <VictoryChart scale={{x: "time"}} className='shooting'>
                    <VictoryLabel x={200} y = {30} text="Shooting Percentage" />
                            <VictoryScatter 
                            data= { shooting }
                            x='date'
                            y='shooting_percentage'
                            domain= {{y: [0,100]}}
                        />
                    </VictoryChart>
                    }

                </div>
            </div>

        </div>

    )

}


export default Dashboard