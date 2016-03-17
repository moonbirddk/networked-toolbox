$(document).on("click", "#btn-resource-list", function(){
  $('.resource-box').toggleClass('expanded');
  $('#btn-expand').toggleClass('hidden');
  $('#btn-collapse').toggleClass('hidden');
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip(); 
    $('.more').shorten({
      'moreText': 'See more',
      'lessText': '',
      'showChars': 350 
    }); 
});
