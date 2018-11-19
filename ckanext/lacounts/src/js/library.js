$(document).ready(function(){

  /* Helper info */
  /***************/

  // show by default on first visit
  var showHelperLibrary = localStorage.getItem('showHelperLibrary');
  if (showHelperLibrary== null) {
    localStorage.setItem('showHelperLibrary', 1);
    // add class to show helper
    $( "#libraryHelper" ).addClass("display");
  }

});
