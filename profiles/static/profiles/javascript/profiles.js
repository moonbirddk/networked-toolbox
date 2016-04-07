$(document).on("click", "#show-all-stories", function(e){
  e.preventDefault();
  $('.story.hidden').removeClass('hidden');
});
