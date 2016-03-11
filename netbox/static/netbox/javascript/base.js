$(document).on("click", "#btn-resource-list", function(){
  $('.resource-box').toggleClass('expanded');
  $('#btn-expand').toggleClass('hidden');
  $('#btn-collapse').toggleClass('hidden');
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip(); 
    $('.readmore').readmore({
        moreLink: '<a class="readmore-more-link" href="#">See more</a>',
        lessLink: '<a class="readmore-less-link" href="#">Close</a>' 
    });
});
