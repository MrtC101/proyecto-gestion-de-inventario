
import Navbar from "../../components/navbar/Navbar"
import { Outlet } from "react-router-dom"
import Footer from "../../components/footer/Footer"
import Sidebar from "../../components/sidebar/Sidebar"


function Dashboard() {
    return (
        <div className="main">
            <Navbar />
            <div className="container2">
                <div className="menuContainer">
                    <Sidebar />
                </div>
                <div className="contentContainer">
                    <Outlet/>
                </div>
            </div>
            <Footer />
        </div>
    )
}



export default Dashboard