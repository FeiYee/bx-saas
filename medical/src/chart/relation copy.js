import * as d3 from 'd3'

export const relationChart = () => {
  let nodes = [
    {
      id: "0",
      label: "Drugs",
      name: "顺铂"
    },
    {
      id: "1",
      label: "Mechanism",
      name: "人工冬虫夏草"
    },
    {
      id: "0",
      label: "Drugs",
      name: "顺铂"
    },
    {
      id: "1",
      label: "Mechanism",
      name: "人工冬虫夏草"
    },
  ]
  let links = [
    {
        source: "0",
        target: "1",
        relationship: "研究"
      },
  ]
  const width = 1200
  const height = 1200
  const color = '#81C784'
  const collide = d3
    .forceCollide()
    .radius(() => 30)
    .iterations(2)
  const linkLine = d3
    .forceLink(links)
    .id(d => d.id)
    .distance(100)
  const charge = d3
    .forceManyBody()
    // .distanceMax(300)
    .strength(-400)

  const simulation = d3
    .forceSimulation(nodes)
    .force('collide', collide)
    .force('charge', charge)
    .force('link', linkLine)
    .force('center', d3.forceCenter(width / 2, height / 2))

  const svg = d3
    .select('.containers')
    .append('svg')
    .attr('viewBox', [0, 0, width, height])
    .attr('class', 'd3')
    .call(
      d3.zoom().on('zoom', function (event) {
        svg.attr('transform', event.transform)
      })
    )
    .on('dblclick.zoom', () => { }) // 禁止双击放大

  const g = svg
    .append('g')
    .attr('class', 'content')
    .selectAll('g')
    .data(nodes, d => d.name)
    .join('g')


  const link = svg
    .append('g')
    // .attr('class', 'links')
    .attr('class', 'link')
    .attr('stroke', '#d3d3d3')
    .attr('stroke-width', 2)
    .selectAll('path')
    .data(links, function (d) {
      if (typeof d.source === 'object') {
        return d.source.name + '_' + d.relationship + '_' + d.target.name
      } else {
        return d.source + '_' + d.relationship + '_' + d.target
      }
    })
    .join('path')
    .attr('id', function (d) {
      if (typeof d.source === 'object') {
        return d.source.name + '_' + d.relationship + '_' + d.target.name
      } else {
        return d.source + '_' + d.relationship + '_' + d.target
      }
    })

  const dbclickNode = () => {

  }
  const clickNode = () => {

  }
  const drag = (simulation) => {
    const dragstarted = (event) => {

    }
  }
  var node = g
    .append('circle')
    .attr('class', 'node')
    .attr('stroke', '#fff')
    .attr('stroke-width', 1.5)
    .attr('fill', color)
    // .selectAll('circle')
    // .data(nodes, d => d.name)
    // .join('circle')
    .attr('r', d => (d.number ? d.number : 50))
    .on('dblclick', dbclickNode)//双击节点事件
    .on('click', clickNode)//单击节点触发事件
  // .on('mouseover', this.mouseoverNode)
  // .on('mouseout', this.mouseoutNode)
  // .call(drag(simulation))

  g
    .append('title')
    .text(d => d.name)
    .attr('dx', () => 10)
    .attr('dy', 50)

  g
    .append('text')
    .attr('fill', '#ffffff')
    .attr('dx', () => -40)
    .attr('dy', '0.25em')
    .text((d) => d.name)
    // .attr('y', function (d) {
    //   d3.select(this).append('tspan').attr('ix', 0).attr('fill', '#ffffff')
    //     .text(() => d.name)
    // })

  // const nodeText = svg
  //   .append('g')
  //   .attr('fill', '#000000')
  //   // .attr('x', 0)
  //   // .attr('y', 0)
  //   .selectAll('text')
  //   .data(nodes, d => d.name)
  //   .join('text')
  //   .text(d => d.name)
  //   .attr('dx', function () { return this.getBoundingClientRect().width / 2 * (-1) })
  //   .attr('dy', 50)


  simulation.on('tick', () => {
    link.attr('d', function (d) {
      if (d.source.x < d.target.x) {
        return (
          'M ' +
          d.source.x +
          ' ' +
          d.source.y +
          ' L ' +
          d.target.x +
          ' ' +
          d.target.y
        )
      } else {
        return (
          'M ' +
          d.target.x +
          ' ' +
          d.target.y +
          ' L ' +
          d.source.x +
          ' ' +
          d.source.y
        )
      }
    })

    node
      .attr('cx', function (d) {
        if (d.fixed) {
          d.fx = nodes[d.index].x
        }
        return d.x
      })
      .attr('cy', function (d) {
        if (d.fixed) {
          d.fy = nodes[d.index].y
        }
        return d.y
      })

    // this.nodesName.attr('x', d => d.x).attr('y', d => d.y)

    d3.selectAll('text')
      .attr('x', d => d.x)
      .attr('y', d => d.y)

    d3.selectAll('tspan')
      .attr('x', d => d.x)
      .attr('y', function (d) {
        return d.y + (this.getAttribute('ix') * 50)
      })

  })
}
