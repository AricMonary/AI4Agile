var treeLayout = {
    name: 'breadthfirst',
    fit: true, // whether to fit the viewport to the graph
    padding: 10, // padding on fit
    avoidOverlap: true, // prevents node overlap, may overflow boundingBox if not enough space
    spacingFactor: 0.45, // positive spacing factor, larger => more space between nodes
    directed: true, // whether the tree is directed downwards (edges can point any direction if false)
    roots: undefined
}