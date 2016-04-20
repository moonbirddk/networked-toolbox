$(document).on("click", "#show-all-stories", function(e){
  e.preventDefault();
  $('.story.hidden').removeClass('hidden');
  $('#show-all-stories').hide();
});
