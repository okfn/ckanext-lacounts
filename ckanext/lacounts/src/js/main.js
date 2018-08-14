$(document).ready(function(){

  /* Search */
  /**********/

  // add default class
  $('.page').addClass( "inactive-search" );

  // make the label / icon tabbable
  $('.masthead .site-search label').attr('tabindex', '0');

  // toggle classes to reveal search modal, add button to close it, and redirect the tabs
  function openSearch() {
    $('.page').addClass( "active-search" );
    $('.page').removeClass( "inactive-search" );
    $(".site-search").append('<button class="close"><i class="fa fa-times" aria-hidden="true"></i><span class="sr-only">Close</span></button>');

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
  }

  // do that on click
  $( ".inactive-search .masthead .site-search label" ).on( "click", function() {
    openSearch();
  });

  // and on Enter
  $( ".inactive-search .masthead .site-search label" ).on( "keypress", function(e) {
    if (e.which == 13) {
      openSearch();
      $('#field-sitewide-search').focus();
    }
  });

  // TODO: figure out why the above two calls run even when inactive-search is replaced with active-search on the .page element.

  // toggle classes to hide search modal, and remove the close button
  function closeSearch() {
    $('.page').addClass( "inactive-search" );
    $('.page').removeClass( "active-search" );
    $( ".masthead .site-search .close" ).remove();
  }

  // do that on click
  $( ".active-search .masthead .site-search .close" ).on( "click", function() {
    closeSearch();
  });

  // and on Enter
  $( ".active-search .masthead .site-search .close" ).on( "keypress", function(e) {
    if (e.which == 13) {
      closeSearch();
    }
  });

  // TODO: figure out why the search form is being submitted when the close button is triggered.

  // TODO: figure out why the above two calls don't work, if tried with a different element (not a button) to avoid submitting the form (see comment above).


  /* Header */
  /**********/

  // use BS affix to detet if scrolled
  $('.masthead').affix();

});
