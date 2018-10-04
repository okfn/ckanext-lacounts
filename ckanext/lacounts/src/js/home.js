$(document).ready(function(){

  /* Twitter feed */
  /****************/

  var configTweet = {
    "profile": {"screenName": 'LA_COUNTS'},
    "domId": 'tweet',
    "maxTweets": 1,
    "showRetweet": false,
    "showUser": false,
    "showInteraction": false,
    "showTime": false,
    "showImages": false,
    "lang": 'en'
  };
  twitterFetcher.fetch(configTweet);


  /* Helper info */
  /***************/

  // toggle helper
  $( ".helper-info .header" ).on( "click", function() {
    $(this).parent(".helper-info").toggleClass( "show" );
  });

  // show by default on first visit
  var showHelper = localStorage.getItem('showHelper');
  if (showHelper== null) {
    localStorage.setItem('showHelper', 1);
    // add class to show helper
    $( ".helper-info" ).addClass("show");
  }

});
