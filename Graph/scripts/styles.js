var treeStyle = [
  {
    "selector": "node",
    "css": {
      "background-opacity": 1.0,
      "background-color": "rgb(137,208,245)",
      "border-opacity": 1.0,
      "width": 75.0,
      "text-opacity": 1.0,
      "color": "rgb(0,0,0)",
      "font-family": "sans-serif",
      "font-weight": "normal",
      "shape": "roundrectangle",
      "border-width": 0.0,
      "text-valign": "center",
      "text-halign": "center",
      "border-color": "rgb(204,204,204)",
      "height": 35.0,
      "font-size": 12,
      "content": "data(name)"
    }
  },
  {
    "selector": "node[type = 'Task']",
    "css": {
      "background-color": "rgb(43,156,204)"
    }
  },
  {
    "selector": "node[type = 'Epic']",
    "css": {
      "background-color": "rgb(121,70,232)"
    }
  },
  {
    "selector": "node[type = 'Story']",
    "css": {
      "background-color": "rgb(91,196,29)"
    }
  },
  {
    "selector": "node:selected",
    "css": {
      "background-color": "rgb(112,112,112)"
    }
  },
  {
    "selector": "edge",
    "css": {
      "font-family": "sans-serif",
      "font-weight": "normal",
      "line-color": "rgb(132,132,132)",
      "target-arrow-color": "rgb(132,132,132)",
      "source-arrow-shape": "none",
      "line-style": "solid",
      "color": "rgb(0,0,0)",
      "source-arrow-color": "rgb(0,0,0)",
      "opacity": 1.0,
      "content": "",
      "target-arrow-shape": "triangle",
      'curve-style': 'bezier',
      "font-size": 10,
      "width": 2.0,
      "text-opacity": 1.0
    }
  },
  {
    "selector": "edge:selected",
    "css": {
      "line-color": "rgb(0,0,0)"
    }
  }
]

var clusterStyle = [
  {
      selector: "node",
      style: {
          "label": "data(name)",
          "font-size" : 12,
          "font-weight" : "normal",
          "border-color" : "rgb(220,220,220)",
          "border-width": 1,
          "text-halign": "center",
          "text-valign": "center"
      }
  },
  {
      selector: ".Epic",
      style: {
          "background-color" : "rgb(121,70,232)",
          "color" : "rgb(0,0,0)",
          "shape": "round-rectangle",
          "label": "data(name)",
          "font-size" : 14,
          "width": "100px"
      }
  },
  {
      selector: ".Story",
      style: {
          "background-color" : "rgb(91,196,29)",
          "color" : "rgb(0,0,0)",
          "shape": "round-rectangle",
          "label": "data(name)",
          "font-size" : 14,
          "width": "100px"
      }
  },
  {
      selector: ".Task",
      style: {
          "background-color" : "rgb(43,156,204)",
          "color" : "rgb(0,0,0)",
          "shape": "round-rectangle",
          "label": "data(name)",
          "font-size" : 14,
          "width": "100px"
      }
  },
  {
      selector: ".assignee",
      style: {
          "background-color": "black",
          "font-size" : 16,
          "color" : "rgb(255,255,255)",
          "shape": "ellipse",
          "label": "data(name)",
          "width": "50px",
          "height": "50px"
      }
  },
  {
      selector: "edge",
      style: {
          "width": 3,
          "line-color" : "rgb(102,102,102)",
          "source-arrow-shape" : "none",
          "target-arrow-shape" : "triangle",
          "target-arrow-color" : "rgb(102,102,102)",
          'curve-style': 'bezier',
          "arrow-scale": 1,
          "border-color" : "rgb(255, 255, 255)",
          "border-width": 1
      }
  }
]