
import { Link } from "react-router-dom"
import "./sidebar.scss"
import { Accordion} from "react-bootstrap";
import {data as sideBarContent} from "../../data/data.tsx";

function Sidebar() {

    return (
        <div className="sidebar">
            {sideBarContent.map((section) => (
                <div className="section" key={section.id}>
                    <span className="sectionTitle">{section.title}</span>
                    {section.modules.map((module, index) => (
                        <Accordion key={index}>
                            <Accordion.Item eventKey="1">
                                <Accordion.Header>
                                    <Link to={module.url} className="module" key={module.id}>
                                        <img src={module.icon} alt="" />
                                        <span className="moduleTitle">{module.title}</span>
                                    </Link>
                                </Accordion.Header>
                                
                                {module.tables && module.tables.length > 0 && ( // Verifica si module.items existe y tiene elementos
                                    <Accordion.Body>
                                        {module.tables?.map((item,index)=>(
                                        <Link key={index} to={item.url} className="item">
                                            <span className="itemTitle">{item.title}</span>
                                        </Link>
                                        ))}
                                    </Accordion.Body>
                                )}

                            </Accordion.Item>
                        </Accordion>
                    ))}
                </div>
            ))}
        </div>
    );    
};

export default Sidebar