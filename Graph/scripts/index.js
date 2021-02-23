/* // source: https://github.com/IlievskiV/Amusive-Blogging-N-Coding/tree/master/JavaScript%20Visualization%20Zoo/Graphs
(function(){
  document.addEventListener('DOMContentLoaded', function(){

    let tryPromise = fn => Promise.resolve().then( fn );

    let toJson = obj => obj.json();
    let cy; 

    let $stylesheet = "styles.json";
    let getStylesheet = name => {
      let convert = res => name.match(/[.]json$/) ? toJson(res) : toText(res);

      return fetch(`styles/${name}`).then( convert );
    };
    let applyStylesheet = stylesheet => { cy.style().fromJson( stylesheet ).update(); };
    let applyStylesheetFromSelect = () => Promise.resolve( $stylesheet ).then( getStylesheet ).then( applyStylesheet );

    let dataset = "networks.json";
    let getDataset = name => fetch(`data/${name}`).then( toJson );
    let applyDataset = dataset => {
      // so new eles are offscreen
      cy.zoom(0.001);
      cy.pan({ x: -9999999, y: -9999999 });
      
      // replace eles
      cy.elements().remove();
      cy.add( dataset );
    }
    let applyDatasetFromSelect = () =>  Promise.resolve( dataset ).then( getDataset ).then( applyDataset );

    let layout = {
      layout: {
        name: 'dagre',
        fit: true, // whether to fit to viewport
        padding: 20
      }
    };
    let prevLayout;
    let getLayout = name => Promise.resolve( layouts[ name ] );
    let applyLayout = layout => {
      if( prevLayout ){
        prevLayout.stop();
      }

      let l = prevLayout = cy.makeLayout( layout );
      return l.run().promiseOn('layoutstop');
    }
    
    let applyLayoutFromSelect = () => Promise.resolve( layout ).then( getLayout ).then( applyLayout );
  
    cy = window.cy = cytoscape({
      container: $('#cy')
    });

    tryPromise( applyDatasetFromSelect ).then( applyStylesheetFromSelect ).then( applyLayoutFromSelect );
  });
})(); */