var style = [
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