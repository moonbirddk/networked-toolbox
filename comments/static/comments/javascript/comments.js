$(function() {

    function appendComment(whereTo, commentData) {
        console.log("appendComment: ", whereTo);
        var tmpl = $.templates("#comment-item-tmpl");
        var commenthtml = tmpl.render(commentData);
        commentEl = $.parseHTML(commenthtml);
        whereTo.append(commentEl);
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

    function onSubmitBtnClick(event) {
        event.preventDefault();
        console.log("onSubmitBtnClick: ", $(this));
        var thisform = $(this).closest('form');
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
                //var data = $.parseJSON(resp);
                if (resp.ok === true){
                    if (thisform.parent().parent().hasClass('comment-reply-form-box')){
                    //thisform.find('input[name=parent]').val()){
                        console.log("new reply");
                        appendComment(thisform
                                        .closest('.comment-replies'),
                                        resp.comment);
                        thisform.closest('.comment-reply-form-box')
                            .fadeOut(300, function() { $(this).remove(); });
                    } else {
                        console.log("new parent comment");
                        appendComment($('#comment-list'), resp.comment);
                    }
                } else {
                    thistextarea.parent().addClass('has-error');
                    thistextarea.parent().append(getErrorsHtml(resp.errors));
                }
            },
            error: function(resp) {
                console.error(resp);
                alert("Internal Error");
            }
        });
    }

    function onReplyBtnClick(event){
        event.preventDefault();
        console.log("onReplyBtnClick: ", $(this));
        var parent_id = $(this).data('parent');
        var related_object_id = $(this).data('related_object_id');
        var related_object_type = $(this).data('related_object_type');
        var repform = $('#comment-form-box').clone();
        if (repform.attr('id')) {
            repform.removeAttr('id');
        }
        var thisitem = repform.closest('.comment-item');
        thisitem.removeClass('comment-item');
        thisitem.addClass('comment-reply-form-box');

        repform.find('input[name=related_object_id]').val(related_object_id);
        repform.find('input[name=related_object_type]').val(related_object_type);
        repform.find('input[name=parent]').val(parent_id);
        repform.hide();
        if ($(this).closest('.comment-item').next().hasClass('comment-replies-row')){
            var has_form_already = $(this).closest('.comment-item').next().find('.comment-replies').children('.comment-reply-form-box').length;
            console.log("reply clicked - it's parent and has replies - append form to the end of replies: ", has_form_already);
            if (!has_form_already) {
                $(this).closest('.comment-item').next().find('.comment-replies').append(repform);
            }
        } else if($(this).closest('.comment-item').parent().hasClass('comment-replies')) {
            var has_form_already = $(this).closest('.comment-item').parent().children('.comment-reply-form-box').length;
            console.log("reply clicked - it's child and has replies - append form to the end of replies: ", has_form_already);
            if (!has_form_already){
                $(this).closest('.comment-item').parent().append(repform);
            }
        } else {
            console.log("reply clicked - doesn't have replies - append replies box and form");
            var rehtml = '<div class="row comment-replies-row">' +
            '<div class="col-md-2 comment-vline"></div>' +
            '<div class="col-md-10 comment-replies"></div></div>';
            var reEl = $(rehtml);
            reEl.insertAfter($(this).closest('.comment-item'));
            //$(this).parent().parent().append(repform);
            $(this).closest('.comment-item')
                .next('.comment-replies-row')
                .find('.comment-replies').append(repform);
        }
        repform.show('slow');
    }
    if ($('body').data('userIsAuthenticated') === true && 
      $('body').data('userHasVerifiedEmail') === true) {
        $('#comment-list-box').delegate('a.comment-reply-btn', 'click', onReplyBtnClick);
        $('#comment-list-box').delegate('a.comment-submit-btn', 'click', onSubmitBtnClick);
        $('#comment-form-box').delegate('a.comment-submit-btn', 'click', onSubmitBtnClick);
    }
});
