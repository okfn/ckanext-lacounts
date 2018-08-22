$(document).ready(function(){

  /* Twitter feed */
  /****************/

  var tweetsHome = {
    "profile": {"screenName": 'LA_COUNTS'},
    "domId": 'tweets',
    "showInteraction": false
  };
  twitterFetcher.fetch(tweetsHome);

});
