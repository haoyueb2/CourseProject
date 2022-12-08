import React from "react";
import * as d3 from "d3";




/**
 * Top K plot
 * @param {Object} props args
 * @returns html response
 */
const TopKPlot = (props) => {
    const data = props.data


    if (props.col === 'book') {
        return (
            <div>
                {data.map((item, i) => (
                    <div>
                        <text fontSize="100"
                            fill="black">
                            {item['title']}:{'   '}{d3.format(".3f")(item['rating'])}
                        </text>
                        <br></br>
                    </div>
                ))}
            </div>
        );
    } else {
        return (
            <div>
                {data.map((item, i) => (
                    <div>
                        <text fontSize="100"
                            fill="black">
                            {item['name']}:{'   '}{d3.format(".3f")(item['rating'])}
                        </text>
                        <br></br>
                    </div>
                ))}
            </div>
        );
    }

};

export default TopKPlot;