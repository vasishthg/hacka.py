$(function () {
    $(document).scroll(function () {
      var $nav = $(".nav");
      $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
    });
});
if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}

$("#vo-run").click(function() {
  $(".vor-main").slideDown(1000);
});

$("#vo-exit").click(function() {
  $(".vor-main").slideUp(1000);
});