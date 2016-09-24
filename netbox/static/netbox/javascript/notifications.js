function netbox_fill_notification_list(data) {
  var $list = $('#live_notify_list').empty();
  if($list) {
    if(data.unread_list.length == 0) {
      $('<li class="no-notification">')
        .wrapInner('You have no unread notifications')
        .appendTo($list);
      $('#mark_all_notifications_as_read').hide();
    } else {
      $('#mark_all_notifications_as_read').show();
      for (var i=0; i < data.unread_list.length; i++) {
        var notification = data.unread_list[i];
        var notificationData = JSON.parse(notification.data) || {};
        var { actor, verb, description } = notification
        var link = notificationData.actions[0].href;

        actor = '<span class="notification__actor">' + actor + ' </span>';
        verb = '<span class="notification__verb">' + verb + '</span>';
        description = '<span class="notification__text">' + description + '</span>';
        var content = '<div class="no-wrap">' + actor + verb + '</div>' + description;

        var classes = 'notification'

        $('<li class="notification">')
          .wrapInner('<a href="' + link + '">' + content + '</a>')
          .appendTo($list);
      }
    }
  }
}

function fill_notification_badge(data) {
  var $badge = $('#live_notify_badge').addClass('notifications__count--zero');
  if ($badge) {
    if (data.unread_count > 0) {
      $badge.removeClass('notifications__count--zero');
      $badge.html(data.unread_count)
    }
    if (data.unread_count > 9) {
      $badge.html('9+')
    }
  }
}

function mark_all_notifications_as_read() {
  $('.notification').addClass('notification--read');
  console.log('Der skal ske noget mere...');
}
