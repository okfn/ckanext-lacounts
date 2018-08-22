$(document).ready(function(){

  /* Twitter feed */
  /****************/

  function handleTweets(tweets) {
    var x = tweets.length;
     var n = 0;
     var element = document.getElementById('tweets');
     var html = '<ul class="owl-carousel">';
     while(n < x) {
       html += '<li>' + tweets[n] + '</li>';
       n++;
     }
     html += '</ul>';
     element.innerHTML = html;

     $(element).children("ul").owlCarousel({
       items: 1,
       autoHeight: true,
       nav: true,
       dots: false
     });
   }

  var tweetsHome = {
    "profile": {"screenName": 'LA_COUNTS'},
    "domId": '',
    "showInteraction": false,
    "customCallback": handleTweets
  };
  twitterFetcher.fetch(tweetsHome);

});
