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
  var hash = url.substring(url.indexOf("#")+1);
  if (hash) {
    var group = $('#'+hash+'-link');
    toggleCategoryGroup(group);
  }
});
