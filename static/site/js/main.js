// Preload
$(window).on("load", function () {
    $(".preloader").fadeOut("slow");
});

$(document).ready(function () {
    // Page Scrolling - Scrollit
    $.scrollIt({
        topOffset: -50
    });
})