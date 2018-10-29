$(document).ready(function(){

  /* Helper info */
  /***************/

  // toggle helper
  $( ".helper-info .header" ).on( "click", function() {
    $(this).parent(".helper-info").toggleClass( "show" );
  });

  // show by default on first visit
  var showHelper = localStorage.getItem('showHelperLibrary');
  if (showHelper== null) {
    localStorage.setItem('showHelperLibrary', 1);
    // add class to show helper
    $( ".helper-info" ).addClass("show");
  }

});
