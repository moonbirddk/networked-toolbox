$(document).on("click", "#show-all-stories", function(e){
  e.preventDefault();
  $('.story.hidden').removeClass('hidden');
  $('#show-all-stories').hide();
});

$(document).on("click", ".category-toggle-fold", function(e){
  e.preventDefault();
  $(this).find(':first-child').toggleClass('glyphicon-triangle-right');
  $(this).find(':first-child').toggleClass('glyphicon-triangle-bottom');
  $(this).closest('.category-group').next().slideToggle();


});
