var styles = [ {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.8.2",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "default",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "background-opacity" : 1.0,
      "background-color" : "rgb(137,208,245)",
      "border-opacity" : 1.0,
      "width" : 75.0,
      "text-opacity" : 1.0,
      "color" : "rgb(0,0,0)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "shape" : "roundrectangle",
      "border-width" : 0.0,
      "text-valign" : "center",
      "text-halign" : "center",
      "border-color" : "rgb(204,204,204)",
      "height" : 35.0,
      "font-size" : 12,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node[IssueType_A = 'Task']",
    "css" : {
      "background-color" : "rgb(14,180,227)"
    }
  }, {
    "selector" : "node[IssueType_A = 'Epic']",
    "css" : {
      "background-color" : "rgb(153,153,255)"
    }
  }, {
    "selector" : "node[IssueType_A = 'Story']",
    "css" : {
      "background-color" : "rgb(153,255,144)"
    }
  }, {
    "selector" : "node[IssueType_B = 'Task']",
    "css" : {
      "background-color" : "rgb(14,180,227)"
    }
  }, {
    "selector" : "node[IssueType_B = 'Epic']",
    "css" : {
      "background-color" : "rgb(153,153,255)"
    }
  }, {
    "selector" : "node[IssueType_B = 'Story']",
    "css" : {
      "background-color" : "rgb(153,255,144)"
    }
  },{
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(112,112,112)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(132,132,132)",
      "target-arrow-color" : "rgb(132,132,132)",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "opacity" : 1.0,
      "content" : "",
      "target-arrow-shape" : "triangle",
      "font-size" : 10,
      "width" : 2.0,
      "text-opacity" : 1.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(0,0,0)"
    }
  } ]
} ]