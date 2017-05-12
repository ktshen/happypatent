/* Project specific Javascript goes here. */

$(document).ready(function(){

    // Add class "active" to sidebar menu's option, based on current url
    $(function() {
      $('#sidebar-' + location.pathname.split("/")[1]).addClass('active');
    });
});
