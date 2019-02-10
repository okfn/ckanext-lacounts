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

  // use BS affix to detect if scrolled
  $('.masthead').affix({
    offset: 1
  });

  // get header height (without px)
  var padTop = parseInt($('.page').css('padding-top'), 10);


  /* Helper info */
  /***************/

  // toggle helper
  $( ".helper-info .header" ).on( "click", function() {
    $(this).parent(".helper-info").toggleClass( "display" );
  });


  /* Truncate text */
  /*****************/

  // story previews
  $(".stories-list article .text").dotdotdot({});

  // blog previews
  $("body.blog article .text").dotdotdot({
    keep: ".more, .topics"
  });

  // function to set an element's max-height
  $.fn.trunc = function(h) {
    var originalHeight = $(this).height();
    // if taller than h, truncate
    if ( originalHeight > h) {
      $(this).addClass('do truncate');
      $(this).css({"overflow":"hidden", "max-height":h + "px"});
      $(this).after('<a class="trunc-expand">More</a>');
    }
    // expand
    $(this).parent().on('click', '.trunc-expand', function() {
      $(this).siblings('.truncate').css("max-height", originalHeight);
      $(this).siblings('.truncate').removeClass('do');
      $(this).after('<a class="trunc-collapse">Less</a>');
      $(this).remove();
    });
    // collapse
    $(this).parent().on('click', '.trunc-collapse', function() {
      $(this).siblings('.truncate').css("max-height", h + "px");
      $(this).siblings('.truncate').addClass('do');
      $(this).after('<a class="trunc-expand">More</a>');
      $(this).remove();
    });
  };
  // Set dataset description to max 100px
  $('body.dataset .notes').trunc(100);
  // Set topic and publissher description to max 100px
  $('body.details .notes').trunc(100);


  /* Content */
  /**********/

  // Activate select2 widget for related datasets
  $('#field-related-datasets').select2({
    placeholder: 'Click to get a drop-down list or start typing a dataset title'
  });

  // Activate select2 widget for featured stories
  $('#field-featured-stories').select2({
    placeholder: 'Click to get a drop-down list or start typing a story title'
  });

  // Activate select2 widget for featured datasets
  $('#field-featured-datasets').select2({
    placeholder: 'Click to get a drop-down list or start typing a dataset title'
  });

  // Topics
  $('#field-groups-get-involved').select2({
    placeholder: 'Click to get a drop-down list or start typing a topic title'
  })

  // Groups override
  var groups = $('#field-groups_override_controller').val()
  var groupsOverride = JSON.parse($('#field-groups_override').val() || '{}')
  $('#field-groups_override_controller')
    .on('change', function(ev) {
      var desiredGroups = $(ev.target).val();
      groupsOverride.add = desiredGroups.filter(function(group) {return !groups.includes(group);});
      groupsOverride.del = groups.filter(function(group) {return !desiredGroups.includes(group);});
      var value = (groupsOverride.add.length || groupsOverride.del.length) ? JSON.stringify(groupsOverride) : '';
      $('#field-groups_override').val(value);
    })
    .select2({
      placeholder: 'Click to get a drop-down list or start typing a topic title'
    })


  /* Stories lead */
  /* TODO: review by Sam, Adria */
  /* Another option is split on the sever but it requires an html parser for Python */
  /**********************************************************************************/
  $('.story .notes > p:first-of-type')
    .addClass('lead')
    .prependTo($('.story .notes'));


  /* Story embeds */
  // Wrap iframes, to control width
  $( ".ckanext-showcase-notes iframe" ).wrap( "<div class='embed'></div>" );


  /* Story images */
  // Make images clickable to open in new tab
  $( ".ckanext-showcase-notes img")
    .click(function (ev) {window.open($(ev.target).attr('src'), '_blank')})
    .attr('title', 'Click to open')
    .css('cursor', 'pointer')


  /* Publishers hierarchy toggle */
  /*******************************/
  $('#publisher-tree .hierarchy-toggle').click(function () {

    // Get visibility
    var isVisible = $(this).next().is(':visible');

    // Show/hide
    if (isVisible) {
      $(this).next().hide();
      $(this).children('i').addClass('fa-plus-circle').removeClass('fa-minus-circle');
    } else {
      $(this).next().show();
      $(this).children('i').addClass('fa-minus-circle').removeClass('fa-plus-circle');
    }

  })

  /* Publishers filter toggle */
  /****************************/
  $('#publisher-filter .filter-toggle').click(function () {

    // Toogle current
    $(this).parent('li').toggleClass('active');

    // Update publishers
    updatePublishers()

  })

  /* Publishers search */
  /*********************/
  $('#publisher-search .search-input').on('change paste keyup', function () {

    // Update publishers
    updatePublishers();

  })


  /* Publishers update */
  /*********************/
  function updatePublishers() {

    // Get search term
    var searchTerm = $('#publisher-search .search-input').val().toLowerCase();

    // Get active types
    var activeTypes = [];
    $('#publisher-filter .filter-list').children('li.active').each(function () {
      activeTypes.push($(this).children('a').data('publisher-type'));
    })

    // Show/hide publishers
    // TODO: we only show/hide top-level See: #118
    $('#publisher-tree .hierarchy-tree-top > li').each(function() {
      var isPassSearch = $(this).children('a').text().toLowerCase().includes(searchTerm);
      var isPassFilter = activeTypes.includes($(this).data('publisher-type'));
      if (isPassSearch && isPassFilter) {
        $(this).show();
      } else {
        $(this).hide();
      }
    })

    // Add/remove publishers not found
    if ($('#publisher-tree .hierarchy-tree-top > li:visible').length === 0) {
      if ($('#publisher-tree .not-found').length === 0) {
        $('#publisher-tree').append('<p class="not-found">Not found</p>');
      }
    } else {
      $('#publisher-tree .not-found').remove();
    }

  }

  /* jump to top */
  /***************/
  $(window).scroll(function() {
    if (padTop) { // not defined on home page
      var scrollPos = $(window).scrollTop();

      if(scrollPos  > padTop) {
        $('.to-top').addClass('active')
      } else {
        $('.to-top').removeClass('active')
      }
    }
  });

  /* Get Involved */
  /****************/
  $('.getinvolved .toggle_description').on('click', function(ev) {
    var desc = $('#' + $(ev.currentTarget).data('target'));
    desc.slideToggle(200);
    ev.currentTarget.blur();
  });



});
