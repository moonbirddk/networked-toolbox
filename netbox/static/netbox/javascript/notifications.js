function netbox_fill_notification_list(data) {
  var $list = $('#live_notify_list').empty();
  if(data.unread_list.length == 0) {
    $('#no-notification').show();
    $('#mark_all_notifications_as_read, #live_notify_list').hide();
  } else {
    $('#no-notification').hide();
    $('#mark_all_notifications_as_read, #live_notify_list').show();
    for (var i=0; i < data.unread_list.length; i++) {
      var notification = data.unread_list[i];
      var notificationData = JSON.parse(notification.data) || {};
      var actor = notification.actor || 'Someone';
      var verb = notification.verb || 'did something';
      var description = notification.description || '';

      actor = '<span class="notification__actor">' + actor + ' </span>';
      verb = '<span class="notification__verb">' + verb + '</span>';
      description = '<span class="notification__text">' + description + '</span>';
      var content = '<div class="no-wrap">' + actor + verb + '</div>' + description;

      $notification = $('<li class="notification">');
      if (notificationData.actions && notificationData.actions.length > 0) {
        var link = notificationData.actions[0].href;
        $notification.wrapInner('<a href="' + link + '">' + content + '</a>');
      }
      $notification.appendTo($list);
    }
  }
  // Unhide the dropdown when the data is loaded
  $('.notifications__dropdown').removeClass('hidden');
}

function fill_notification_badge(data) {
  var $badge = $('#live_notify_badge');

  if(data.unread_count <= 0) {
    $badge.addClass('notifications__count--zero');
    $badge.html('');
  } else if (data.unread_count > 9) {
    $badge.removeClass('notifications__count--zero');
    $badge.html('9+');
  } else {
    $badge.removeClass('notifications__count--zero');
    $badge.html(data.unread_count);
  }
}

function mark_all_notifications_as_read() {
  $('.notification').addClass('notification--read');
  // Send a notification to the API
  $.get('/inbox/notifications/mark-all-as-read/')
  .done(function() {
    // Fetch the notifications data again
    fetch_api_data();
  });
}
