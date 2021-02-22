// source: https://github.com/IlievskiV/Amusive-Blogging-N-Coding/tree/master/JavaScript%20Visualization%20Zoo/Graphs
(function(){
    document.addEventListener('DOMContentLoaded', function(){
      let $ = selector => document.querySelector( selector );
  
      let tryPromise = fn => Promise.resolve().then( fn );
  
      let toJson = obj => obj.json();
      let toText = obj => obj.text();
  
      let cy; 
  
      let $stylesheet = "styles.js";
      let getStylesheet = name => {
        let convert = res => name.match(/[.]json$/) ? toJson(res) : toText(res);
  
        return fetch(`scripts/${name}`).then( convert );
      };
      let applyStylesheet = stylesheet => {
        if( typeof stylesheet === typeof '' ){
          cy.style().fromString( stylesheet ).update();
        } else {
          cy.style().fromJson( stylesheet ).update();
        }
      };
      let applyStylesheetFromSelect = () => Promise.resolve( $stylesheet ).then( getStylesheet ).then( applyStylesheet );
  
      let $dataset = "networks.js";
      let getDataset = name => fetch(`scripts/${name}`).then( toJson );
      let applyDataset = dataset => {
        // replace eles
        cy.elements().remove();
        cy.add( dataset );
      }
      let applyDatasetFromSelect = () => 
            Promise.resolve( $dataset ).then( getDataset ).then( applyDataset );
  
      let $layout = "dagre";
      let layouts = {
        layout: {
          name: 'dagre',
          fit: true, // whether to fit to viewport
          padding: 30,
          animate: false
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
      let applyLayoutFromSelect = () => Promise.resolve( $layout ).then( getLayout ).then( applyLayout );
    
      cy = window.cy = cytoscape({
        container: $('#cy')
      });
  
      tryPromise( applyDatasetFromSelect ).then( applyStylesheetFromSelect ).then( applyLayoutFromSelect );
    });
  })();