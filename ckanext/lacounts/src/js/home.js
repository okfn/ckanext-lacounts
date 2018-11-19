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

  // show by default on first visit
  var showHelper = localStorage.getItem('showHelper');
  if (showHelper== null) {
    localStorage.setItem('showHelper', 1);
    // add class to show helper
    $( "#featuredvisHelper" ).addClass("display");
  }


  /* Banner images */
  /*****************/

  function setImage(id, elementReady) {

    function elementReady(id) {
      var e = document.getElementById(id);
      e.className += " ready";
    }

    var bannerImages = [
      "images/banner1.jpg",
      "images/banner2.jpg",
      "images/banner3.jpg",
      "images/banner4.jpg"
    ];

    var imgCount = bannerImages.length;
    var imgNumber = Math.floor(imgCount*Math.random());

    document.getElementById(id).src=bannerImages[imgNumber];

    elementReady(id);
  }

  if ( $(".navbar-toggle").css("display") == "none" ) {
    // not small screens
    setImage("BannerImage");
  }


  /* Featured Visualisation */
  /**************************/

  // toggle BS collapse on description
  $(".featured-visualisation .toggle").on("click", function() {
    $(this).parents(".caption-header").toggleClass("show-as-collapsed");
    $(this).parents("figcaption").children(".caption-body").collapse('toggle');
  });

});
