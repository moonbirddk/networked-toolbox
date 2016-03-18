$(document).on("click", "#btn-resource-list", function(){
  $('.resource-box').toggleClass('expanded');
  $('#btn-expand').toggleClass('hidden');
  $('#btn-collapse').toggleClass('hidden');
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip(); 
    $('.tool-more').shorten({
      'moreText': 'See more',
      'showChars': 1500 
    }); 
    $('.story-more').shorten({
      'moreText': 'See more',
      'showChars': 250 
    }); 
});
