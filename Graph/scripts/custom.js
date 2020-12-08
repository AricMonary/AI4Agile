$( document ).ready(function(){
  // Custom Cytoscape.JS code goes here.  
  // Example: add linkouts to nodes that opens the "href" node attribute on click
  cy.on('tap', 'node', function(){
     try { // your browser may block popups
       window.open( this.data('href') );
     } catch(e){ // fall back on url change
       window.location.href = this.data('href');
     }
  });

  /*function makePopper(ele) {
    let ref = ele.popperRef(); // used only for positioning
  
    ele.tippy = tippy(ref, { // tippy options:
      content: () => {
        //let content = document.createElement('div');
        let content = "test"
        //content.innerHTML = ele.id();
  
        return content;
      },
      trigger: 'manual' // probably want manual mode
    });
  }

  cy.elements().forEach(function(ele) {
    makePopper(ele);
  });
  cy.on('mouseover', (event) => event.target.tippy.show());
  cy.on('mouseout', (event) => event.target.tippy.hide());*/
  
  var eles = cy.elements();
  cy.fit(eles)
  cy.center(eles)
  cy.maxZoom(1.6)
  cy.minZoom(0.96)
  //cy.elements().shift('x', -50);
});

/*$( window ).ready(function(){
  cy.on('resize', function(event){
    cy.center();
  });
});*/