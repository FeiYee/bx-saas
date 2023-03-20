import * as d3 from 'd3'

export const relationChart = (data, handleNodeClick) => {
  let nodes = data.nodes || [
    {
      id: "0",
      label: "Drugs",
      name: "顺铂"
    },
    {
      id: "1",
      label: "Mechanism",
      name: "人工冬虫夏草",
      Type: "Machine",
      Year: "2019-12-11"
    },
    {
      id: "2",
      label: "Drugs",
      name: "Cordycepin Increases Nonrapid Eye Movement Sleep via Adenosine Receptors in Rats"
    },
    {
      id: "3",
      label: "Mechanism",
      Type: "Artificial",
      name: "人工冬虫夏草"
    },
  ]
  let links = data.links || [
    {
      source: "0",
      target: "1",
      relationship: "研究"
    },
  ]

  let selector = '#chartRelationship'
  d3.select(selector).selectAll('*').remove();

  const width = 1254
  const height = 904
  const color = '#67c23a'

  // 碰撞作用力，为节点指定一个radius区域来防止节点重叠，设置碰撞力的强度，范围[0,1], 默认为0.7。设置迭代次数，默认为1，迭代次数越多最终的布局效果越好，但是计算复杂度更高
  const collide = d3
    .forceCollide(100)
    .radius(() => 30)
    .strength(0.7)
    .iterations(3)
  const linkLine = d3
    .forceLink(links)
    .id(d => d.id)
    .distance(200)
  // 万有引力
  const charge = d3
    .forceManyBody()
    .strength(-800)
    .distanceMax(300)

  const simulation = d3
    .forceSimulation(nodes)
    .force('collide', collide)
    .force('charge', charge)
    .force('link', linkLine)
    .force('center', d3.forceCenter(width / 2, height / 2))

  const svg = d3
    .select(selector)
    .append('svg')
    .attr('viewBox', [0, 0, width, height])
    .attr('class', 'd3')
    .call(
      d3.zoom().scaleExtent([0.1, 2]).on('zoom', function (event) {
        // svg.attr('transform', event.transform)
        // if (event.transform.k > 1) {
        //   svg.attr('transform', event.transform)
        // } else {
        //   svg.attr("transform", "scale(" + event.transform.k + ")");
        // }
        // svg.attr("transform", "scale(" + event.transform.k + ")");
        svg.selectAll("g").attr('transform', event.transform)
      })
    )
    .on('dblclick.zoom', () => { }) // 禁止双击放大


  const marker = svg
  .append('defs')
    .append('marker')
    .attr('id', 'marker')
    .attr('markerUnits', 'userSpaceOnUse')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 59)
    .attr('refY', 0)
    .attr('makerWidth', 8)
    .attr('markerHeight', 8)
    .attr('orient', 'auto')
    .attr('stroke-width', 2)
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#e3e3e3')


  const link = svg
    .append('g')
    .attr('class', 'link')
    .attr('stroke', '#d3d3d3')
    .attr('stroke-width', 2)
    .selectAll('path')
    // .data(links, function (d) {
    //   if (typeof d.source === 'object') {
    //     return d.source.name + '_' + d.relationship + '_' + d.target.name
    //   } else {
    //     return d.source + '_' + d.relationship + '_' + d.target
    //   }
    // })
    .data(links)
    .enter()
    .append('path')
  // .attr('id', function (d) {
  //   if (typeof d.source === 'object') {
  //     return d.source.name + '_' + d.relationship + '_' + d.target.name
  //   } else {
  //     return d.source + '_' + d.relationship + '_' + d.target
  //   }
  // })

  const dbclickNode = () => {

  }
  const clickNode = (e, d) => {
    console.log(d, e)
    handleNodeClick(d)
  }
  const drag = (simulation) => {
    const dragstarted = (event) => {

    }
  }
  const node = svg
    // .append('g')
    // .attr('class', 'content')
    // .attr("width", width)
    // .attr("height", height)
    .selectAll('circle')
    // .data(nodes, d => d.name)
    .data(nodes)
    .enter()
    .append('g')
    .attr('class', 'node')
    .on('dblclick', dbclickNode)//双击节点事件
    .on('click', clickNode)//单击节点触发事件
    .call(d3.drag()
      .on('start', function (event, d) {
        event.sourceEvent.stopPropagation();
        // restart()方法重新启动模拟器的内部计时器并返回模拟器。
        // 与simulation.alphaTarget或simulation.alpha一起使用时，此方法可用于在交互
        // 过程中进行“重新加热”模拟，例如在拖动节点时，在simulation.stop暂停之后恢复模拟。
        // 当前alpha值为0，需设置alphaTarget让节点动起来
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      })
      .on('drag', function (event, d) {

        // d.fx属性- 节点的固定x位置
        // 在每次tick结束时，d.x被重置为d.fx ，并将节点 d.vx设置为零
        // 要取消节点，请将节点 .fx和节点 .fy设置为空，或删除这些属性。
        d.fx = event.x;
        d.fy = event.y;
      })
      .on('end', function (event, d) {

        // 让alpha目标值值恢复为默认值0,停止力模型
        // if (!d.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }));


  const circle = node
    .append('circle')
    .attr('stroke', '#d1edc4')
    .attr('stroke', d => {
      let color = '#d1edc4'
      if (d.Type === 'Artificial') {
        // color = '#f3d19e'
      } else if (d.Type === 'Machine') {
        color = '#a0cfff'
      }
      return color
    })
    .attr('stroke-width', 6)
    .attr('fill', color)
    .attr('fill', d => {
      let color = '#67c23a' // 绿色
      if (d.Type === 'Artificial') {
        // color = '#e6a23c'   // 黄色
      } else if (d.Type === 'Machine') {
        color = '#409eff'   // 蓝色
      }
      return color
    })
    .attr("opacity", "0.6")
    .style("cursor", "pointer")
    .attr('r', d => {
      let radius = 56
      let now = new Date()
      let date = new Date()
      if (d.Year) {
        try {
          date = new Date(d.Year)
        } catch (e) {}
        if (date.getFullYear() + 2 < now.getFullYear()) {
          radius = 40
        }
      }
      return radius
    })
    // .selectAll('circle')
    // .data(nodes, d => d.name)
    // .join('circle')
    // .on('mouseover', this.mouseoverNode)
    // .on('mouseout', this.mouseoutNode)
    // .call(drag(simulation))

  const title = node
    .append('title')
    .text(d => d.name)
    .attr('dx', () => 10)
    .attr('dy', 50)

  const text = node
  // .append('rect')
  //   .attr('width', 100)
  //   .attr('height', 100)
  //   .attr('fill', '#ffffff')
    // .attr("opacity", "0.5")
    // .attr('x', 0)
    // .attr('y', 0)
    .append('text')
    .attr('fill', '#333333')
    // .attr("opacity", "0.5")
    .style("font-size", 14)
    .style("cursor", "pointer")
    .attr('dx', () => -40)
    .attr('dy', -26)
    // .text((d) => d.name)
    .attr('x', function (d) {
      const len = 12
      const step = 5
      let title = d.title || d.Title || d.name || ''
      // let titles = title.split(' ')
      let title1 = ''
      let title2 = ''
      let title3 = ''
      let title4 = ''
      let title5 = ''
      let title6 = ''
      title1 = title.substring(0, len)
      title2 = title.substring(len, len * 2 + step)
      title3 = title.substring(len * 2, len * 3 + step * 2)
      title4 = title.substring(len * 3, len * 4 + step)
      title5 = title.substring(len * 4, len * 5)

      if (title.length > 0) {

      }

      d3.select(this)
        .append('tspan')
        // .attr('ix', 0)
        // .attr('fill', '#000000')
        .text(title1)

      if (title2) {
        d3.select(this)
        .append('tspan')
        // .attr('ix', 0)
        .attr('dx', -58)
        .attr('dy', -12)
        // .attr('fill', '#000000')
        .text(title2)
      }
      if (title3) {
        d3.select(this)
        .append('tspan')
        .attr('dx', -68)
        .attr('dy', 2)
        .text(title3)
      }
      if (title4) {
        d3.select(this)
        .append('tspan')
        .attr('dx', -58)
        .attr('dy', 16)
        .text(title4)
      }
      if (title5) {
        d3.select(this)
        .append('tspan')
        .attr('dx', -40)
        .attr('dy', 30)
        .text(title5)
      }
    })

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
        return ('M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y)
      } else {
        return ('M ' + d.target.x + ' ' + d.target.y + ' L ' + d.source.x + ' ' + d.source.y)
      }
    })

    d3.selectAll('circle')
      .attr('cx', function (d) {
        if (!d) {
          return
        }
        if (d.fixed) {
          d.fx = nodes[d.index].x
        }
        return d.x
      })
      .attr('cy', function (d) {
        if (!d) {
          return
        }
        if (d.fixed) {
          d.fy = nodes[d.index].y
        }
        return d.y
      })


    d3.selectAll('text')
      .attr('x', d => d.x)
      .attr('y', d => d.y)

      d3.selectAll('rect')
      .attr('x', d => d.x - 50)
      .attr('y', d => d.y - 50)

    d3.selectAll('tspan')
      .attr('x', d => d.x)
      .attr('y', function (d) {
        return d.y + (this.getAttribute('ix') * 50)
      })

  })
}
