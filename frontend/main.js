import Axios from "axios"
import * as d3 from "d3"
import {curry,prop,compose,map} from "ramda"
import {point,vector} from "@flatten-js/core"

const drag = simulation => {
   function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
         event.subject.fx = event.subject.x;
         event.subject.fy = event.subject.y;
   }

   function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
   }

   function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
         event.subject.fx = null;
         event.subject.fy = null;
   }

   return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
}

const zoom_handler_for = (el) => { 
      return d3.zoom()
         .on("zoom",(e)=>{
            el.attr("transform",e.transform)
         })
   }

const make_plot = (size,root_node,data) =>{
   let ratio = 1.5 
   let width = size * ratio
   let height = size

   let mheight = 5 
   let mwidth = 7 
   let edge_color = "#44f"
   let node_color = "#55f"
   let background_color = "#ccc"
   let node_radius = 6

   let root = d3.select(root_node)
      .append("svg")
      .attr("id","plot")
      .attr("viewBox",[0,0,width,height])


   root.append("rect")
      .attr("width","100%")
      .attr("height","100%")
      .attr("fill",background_color)

   let plot = root.append("g")
   zoom_handler_for(plot)(root)

   plot.append("defs").append("marker")
      .attr("id","head")
      .attr("orient","auto")
      .attr("markerWidth",mwidth)
      .attr("markerHeight",mheight)
      .attr("refX",mwidth+node_radius/2)
      .attr("refY",mheight/2)
      .append("path")
         .attr("d",d3.line()([[0,0],[0,mheight],[mheight,mheight/2]]))
         .attr("fill",edge_color)

   let sim = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink(data.links).id(d => d.id))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(width / 2, height / 2))

   const link = plot.append("g")
      .attr("stroke", edge_color)
      .attr("stroke-opacity", 0.6)
      .selectAll("line")

      .data(data.links)
      .join("line")
      .attr("stroke-width", d => Math.sqrt(d.value))
      .attr("marker-end","url(#head)")

   const link_annotation = plot.append("g")
      .selectAll("text")
      .data(data.links)
      .join("text")
      .text(d=>d.reference)
      .attr("font-size","5px")
      .attr("text-anchor","middle")

   let node = plot.append("g")
      .attr("class","nodes")
      .selectAll(".node")
      .data(data.nodes)
      .enter()
      .append("g")
      .attr("class","node")
      .call(drag(sim))

   node.append("circle")
      .attr("r", node_radius)
      .attr("fill", node_color)

   node.append("g")
      .attr("class","textbox")
      .append("text")
      .text(d=>d.id)
      .attr("font-size","5px")
      .attr("transform",`translate(${node_radius},1)`)

   sim.on("tick", () => {
      link
         .attr("x1", d => d.source.x)
         .attr("y1", d => d.source.y)
         .attr("x2", d => d.target.x)
         .attr("y2", d => d.target.y)

      link_annotation
         .attr("x",e=>(e.source.x + e.target.x)/2)
         .attr("y",e=>(e.source.y + e.target.y)/2)

      node
         .attr("transform",d=>`translate(${d.x},${d.y})`)
   })
}


Axios.get("/graph")
   .then((r)=>{
      make_plot(300,"#app",r.data)
   })
