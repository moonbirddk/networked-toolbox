$(document).on("click", "#show-all-stories", function(e){
  e.preventDefault();
  $('.story.hidden').removeClass('hidden');
  $('#show-all-stories').hide();
});

function toggleCategoryGroup(group) {
  group.find(':first-child').toggleClass('glyphicon-triangle-right');
  group.find(':first-child').toggleClass('glyphicon-triangle-bottom');
  group.closest('.category-group').next().slideToggle();
}

$(document).on("click", ".category-toggle-fold", function(e){
  e.preventDefault();
  toggleCategoryGroup($(this));
});

$(document).ready(function(){
  var url = $(location).attr('href');
  var i = url.indexOf("#");
  if (i != -1) {
    var hash = url.substring(i+1);
    var group = $('#'+hash+'-link');
    toggleCategoryGroup(group);
  }
});
