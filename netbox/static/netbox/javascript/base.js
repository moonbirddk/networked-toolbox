$(document).on("click", "#btn-resource-list", function(){
  $('.resource-box').toggleClass('expanded');
  $('#btn-expand').toggleClass('hidden');
  $('#btn-collapse').toggleClass('hidden');
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip(); 
    $('.more').shorten({
      'moreText': 'Read more',
      'showChars': 1500 
    }); 
    $('.category-more').shorten({
      'moreText': 'Read more',
      'showChars': 550
    }); 
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
