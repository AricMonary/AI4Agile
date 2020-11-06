/* App frontend script */
AP.events.on('ISSUE_QUICK_ADD_CLICKED', function(event){
  AP.dialog.create({
        key: 'sized-panel',
        width: '500px',
        height: '200px',
        chrome: true,
        header: JSON.stringify(event)
  });
});
