$(document).ready(function(){

  /* Search */
  /**********/

  // add default class
  $('.page').addClass( "inactive-search" );

  // make the label / icon tabbable
  $('.masthead .site-search label').attr('tabindex', '0');

  // toggle classes to hide search modal, and remove the close button
  function closeSearch() {
    $('.page').addClass( "inactive-search" );
    $('.page').removeClass( "active-search" );
    $( ".masthead .site-search .close" ).remove();
  }

  // toggle classes to reveal search modal, add button to close it, and redirect the tabs
  function openSearch() {
    $('.page').addClass( "active-search" );
    $('.page').removeClass( "inactive-search" );
    $(".site-search").append('<button class="close" type="button"><i class="fa fa-times" aria-hidden="true"></i><span class="sr-only">Close</span></button>');

    // set first and last tabbable elements
    var firstInput = $('.active-search #field-sitewide-search');
    var lastInput = $('.active-search .masthead .site-search .close');

    // redirect last tab to first input
    lastInput.on('keydown', function (e) {
      if ((e.which === 9 && !e.shiftKey)) {
        e.preventDefault();
        firstInput.focus();
      }
    });

    // redirect first shift+tab to last input
    firstInput.on('keydown', function (e) {
      if ((e.which === 9 && e.shiftKey)) {
        e.preventDefault();
        lastInput.focus();
      }
    });

    // close search on click
    $( ".active-search .masthead .site-search .close" ).on( "click", function() {
      closeSearch();
    });

    // close search on Enter
    $( ".active-search .masthead .site-search .close" ).on( "keypress", function(e) {
      if (e.which == 13) {
        closeSearch();
      }
    });
  }

  // open search on click
  $( ".inactive-search .masthead .site-search label" ).on( "click", function() {
    openSearch();
  });

  // open search on Enter
  $( ".inactive-search .masthead .site-search label" ).on( "keypress", function(e) {
    if (e.which == 13) {
      openSearch();
      $('#field-sitewide-search').focus();
    }
  });

  // TODO: figure out why the above two calls run even when inactive-search is replaced with active-search on the .page element.


  /* Header */
  /**********/

  // use BS affix to detet if scrolled
  $('.masthead').affix();


  /* Featured Visualisation */
  // toggle BS collapse on description
  $(".featured-visualisation .toggle").on("click", function() {
    $(this).toggleClass("show-as-collapsed");
    $(this).parents("figcaption").children(".caption-body").collapse('toggle');
  });

});
