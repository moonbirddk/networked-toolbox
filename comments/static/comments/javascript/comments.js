$(function() {

    function appendComment(commentData) {
        var tmpl = $.templates("#comment-item-tmpl");
        var html = tmpl.render(commentData);
        $('#comment-list').append(html);
    }
    
    $(".comment-submit-btn").click(function(event) {
        event.preventDefault();
        console.log("comment submit clicked");
        var thisform = $(this).parent().parent();
        var csrftoken = getCookie('csrftoken');
        var postdata = thisform.serialize();
        thisform.find('textarea').val('');
        postdata += '&csrfmiddlewaretoken=' + csrftoken
        console.log(postdata);
        
        $.ajax({
            type: 'POST',
            url: window.COMMENTS_ADD_COMMENT_URL,
            data: postdata,
            cache: false,
            success: function (resp) {
                console.log(resp);
                //var data = $.parseJSON(resp);
                if (resp.ok === true){
                    //location.reload();
                    appendComment(resp.comment);
                } else {
                    alert(resp.errors);
                }
            },
            error: function(resp) {
                console.log(resp);
                alert(resp.responseText);
            }
        });
    });
});