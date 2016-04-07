$(function() {

    function appendComment(commentData) {
        var tmpl = $.templates("#comment-item-tmpl");
        var html = tmpl.render(commentData);
        $('#comment-list').append(html);
    }
    
    function getErrorsHtml(errors) {
        // '<span class="help-block">content: This field is required.</span>'
        var html = '';
        $.each(errors, function(fname, ferrors){
            $.each(ferrors, function(ferrkey, ferror){
                console.log(ferror);
                html += '<span class="help-block">' + fname + ': ' + ferror.message + '<span>';
            });
        });
        return html;
    }
    
    $(".comment-submit-btn").click(function(event) {
        event.preventDefault();
        var thisform = $(this).parent().parent();
        var csrftoken = getCookie('csrftoken');
        var postdata = thisform.serialize();
        var thistextarea = thisform.find('textarea');
        postdata += '&csrfmiddlewaretoken=' + csrftoken;
        
        $.ajax({
            type: 'POST',
            url: window.COMMENTS_ADD_COMMENT_URL,
            data: postdata,
            cache: false,
            success: function (resp) {
                thistextarea.val('');
                thistextarea.parent().removeClass('has-error');
                thistextarea.parent().find('.help-block').remove();
                console.log(resp);
                //var data = $.parseJSON(resp);
                if (resp.ok === true){
                    appendComment(resp.comment);
                } else {
                    thistextarea.parent().removeClass('has-error');
                    thistextarea.parent().find('.help-block').remove();
                    
                    thistextarea.parent().addClass('has-error');
                    thistextarea.parent().append(getErrorsHtml(resp.errors));
                }
            },
            error: function(resp) {
                console.error(resp);
                alert("Internal Error");
            }
        });
    });
});