import * as echarts from 'echarts';


export function getRelationData(data) {
  let nodes = data.nodes
  let links = data.links
  let relationData = {
    nodes: [],
    links: []
  }

  let nodeDatas = []
  let linkDatas = []
  let nodeIds = []

  nodes.forEach(node => {
    let item = node.data
    if (nodeIds.includes(item.id)) {
      return
    }
    nodeIds.push(item.id)
    nodeDatas.push(item)
  })

  links.forEach(link => {
    let item = link.data
    item.name = item.relationship
    item.source = item.source + ''
    item.target = item.target + ''

    linkDatas.push(item)
  })

  relationData = {
    nodes: nodeDatas,
    links: linkDatas
  }

  return relationData
}



export const setChartRelation = function (data, domId, clickFn) {
  const dom = document.getElementById(domId)
  let chartRelationship = echarts.getInstanceByDom(dom)
  if (!chartRelationship) {
    chartRelationship = echarts.init(dom);
  }

  data = data || {
    links: [
      // {
      //   source: "0",
      //   target: "1",
      //   relationship: "研究"
      // },
      // {
      //   source: "0",
      //   target: "5",
      //   relationship: "研究"
      // },
      // {
      //   source: "0",
      //   target: "6",
      //   relationship: "研究"
      // },
      // {
      //   source: "0",
      //   target: "7",
      //   relationship: "研究"
      // },
      // {
      //   source: "0",
      //   target: "12",
      //   relationship: "研究"
      // },
    ],
    nodes: [
      // {
      //   id: "0",
      //   label: "Drugs",
      //   name: "顺铂"
      // },
      // {
      //   id: "1",
      //   label: "Mechanism",
      //   name: "人工冬虫夏草"
      // },
      // {
      //   id: "5",
      //   label: "Object",
      //   name: "研究对象"
      // },
      // {
      //   id: "6",
      //   label: "subAuthor",
      //   name: "单娟萍"
      // },
      // {
      //   id: "7",
      //   label: "subAuthor",
      //   name: "沈水娟"
      // },
      // {
      //   id: "12",
      //   label: "Relation",
      //   name: "下降"
      // }

    ]
  }

  var option = {
    // 图的标题
    // title: {
    //   text: '关系图'
    // },
    // 提示框的配置
    tooltip: {
      formatter: function (x) {
        return x.data.title || x.data.name;
      }
    },
    // 工具箱
    toolbox: {
      // 显示工具箱
      show: false,
      feature: {
        mark: {
          show: true
        },
        // 还原
        restore: {
          show: true
        },
        // 保存为图片
        saveAsImage: {
          show: true
        }
      }
    },
    series: [{
      type: 'graph', // 类型:关系图
      layout: 'force', //图的布局，类型为力导图
      symbolSize: 80, // 调整节点的大小
      roam: true, // 是否开启鼠标缩放和平移漫游。默认不开启。若是只想要开启缩放或者平移,能够设置成 'scale' 或者 'move'。设置成 true 为都开启
      edgeSymbol: ['circle', 'arrow'],
      edgeSymbolSize: [2, 10],
      edgeLabel: {
        normal: {
          textStyle: {
            fontSize: 20,
            overflow: 'truncate'

          }
        },
        textStyle: {
          overflow: 'truncate'
        }
      },
      force: {
        repulsion: 2500,
        edgeLength: [10, 50]
      },
      draggable: true,
      lineStyle: {
        normal: {
          width: 2,
          color: '#4b565b',
        }
      },
      edgeLabel: {
        normal: {
          show: true,
          formatter: function (x) {
            let text = x.data.name
            if (text.length > 20) {
              text = text.substring(0, 20) + '...'
            }
            return text;
          },
          textStyle: {
            fontSize: 20,
            overflow: 'truncate'

          }
        },
        textStyle: {
          fontSize: 20,
          overflow: 'truncate'

        }
      },
      label: {
        show: true,
        // position: 'right',
          formatter: '{b}',
          textStyle: {
            fontSize: 20,
            overflow: 'truncate'
          },
          formatter: function (x) {
            let text = x.data.name
            if (text.length > 20) {
              text = text.substring(0, 20) + '...'
            }
            return text;
          },
        // normal: {
        //   show: true,
        //   textStyle: {
        //     overflow: 'truncate'
        //   }
        // },
        // textStyle: {
        //   overflow: 'truncate'
        // }
      },

      // 数据
      data: data.nodes,
      links: data.links,
    }]
  };
  chartRelationship.setOption(option);

  chartRelationship.on('click', param => {
    if (param.dataType === 'node') {
      console.log(param)
      clickFn(param.data)

      if (clickFn instanceof Function) {
      }
    }
  })
  return chartRelationship
}



export const setChartPie = function (domId) {
  const chartDom = document.getElementById(domId);
  let chartPie = echarts.init(chartDom);

  var option = {
    // title: {
    //   text: '',
    //   subtext: 'Fake Data',
    //   left: 'center'
    // },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      bottom: 10,
      left: 'center',
    },
    series: [
      {
        name: 'Access From',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 1048, name: 'Search Engine' },
          { value: 735, name: 'Direct' },
          { value: 580, name: 'Email' },
          { value: 484, name: 'Union Ads' },
          { value: 300, name: 'Video Ads' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };

  chartPie.setOption(option);

  return chartPie
}



export const setChartBar = function (domId) {
  var chartDom = document.getElementById(domId);
  let chartBar = echarts.init(chartDom);

  const option = {
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [120, 200, 150, 80, 70, 110, 130],
        type: 'bar'
      }
    ]
  };

  chartBar.setOption(option);

  return chartBar
}
