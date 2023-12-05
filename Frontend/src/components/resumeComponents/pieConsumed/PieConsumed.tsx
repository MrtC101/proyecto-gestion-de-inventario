import "./pieConsumed.scss"
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { useEffect, useState } from "react";
import { ListItems } from "../../../Api/apiService";
import { setMessage } from "../../providerComponents/messageDisplay/MessageDisplay";
export const PieConsumed = () => {
    const [stats, setStats] = useState([]);

    const prettyColors = ["#fd7f6f", "#7eb0d5", "#b2e061", "#bd7ebe", "#ffb55a", "#ffee65", "#beb9db", "#fdcce5", "#8bd3c7", "#ededc7"]

    useEffect(()=>{
        ListItems(setStats, "stat-consumed")
            .catch((error) => {
                setMessage(`Ha surgido un error al buscar estadísticas.`,error)
            })
    },[setStats])

    const data = stats.map(
        (stat, index) => {
            
            return(
                {
                    name: stat["nombre"],
                    value: stat["cantidadTotal"],
                    color: prettyColors[index % prettyColors.length]
                }
            );
        }
    );

  return (
    <div className="pieChartBox">
        <h1>Insumos más consumidos</h1>
        <div className="chart">
            <ResponsiveContainer width="99%" height={300}>
                <PieChart>
                    <Tooltip
                    contentStyle={{background:"white", borderRadius:"5px"}}
                    />
                    <Pie
                        data={data}
                        innerRadius={"70%"}
                        outerRadius={"90%"}
                        paddingAngle={5}
                        dataKey="value"
                    >
                        {data.map((item) => (
                            <Cell
                            key={item.name} fill={item.color} 
                            />
                        ))}
                    </Pie>
                </PieChart>
            </ResponsiveContainer>
        </div>
        <div className="options">
            {data.map(item=>(
                <div className="option" key={item.name}>
                    <div className="title">
                        <div className="dot" style={{backgroundColor:item.color}} />
                        <span>{item.name}</span>
                    </div>
                    <span>{item.value}</span>
                </div>

            ))}
        </div>
        
    </div>
  )
}
export default PieConsumed