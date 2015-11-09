$(document).on("click", "#btn-resource-list", function(){
  $('.resource-box').toggleClass('expanded');
  $('#btn-expand').toggleClass('hidden');
  $('#btn-collapse').toggleClass('hidden');
});
