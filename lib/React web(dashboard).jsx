import React ,{useEffect,useState} from "react";
import axios from "axios";
function Dashboard(){
    const[stats,setStats]=
    useState({});
    useEffect(() =>{
        axios.get("http://<SERVER_IP>:8000/stats")
        .the(res=>
            setStats(res.data)
        );
    },[]);
    return (
        < div style={{padding:"20xp",background:
            "#of172a",color:"white"
        }}
        >
            <h1>Dashboard</h1>
            <div>revenue:{stats.revenue}</div>
            <div>profil:{stats.profit}</div>
            </div>
    );
}
export default Dashboard;