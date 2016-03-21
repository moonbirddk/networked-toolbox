$(document).ready(function(){
    $('#id_content').summernote({
      toolbar: [
        // [groupName, [list of button]]
        ['insert', ['link', 'picture', 'video']]
      ],
      width: '100%',
      height: '300'
  });
});
