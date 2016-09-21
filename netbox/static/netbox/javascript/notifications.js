function netbox_fill_notification_list(data) {
  var $list = $('#live_notify_list').empty();
  if(data.unread_list) {
    for (var i=0; i < data.unread_list.length; i++) {
      var notification = data.unread_list[i];
      var notificationData = JSON.parse(notification.data) || {};

      console.log('notification #' + i + ': ', notification);
      var $actor = $('<span>').text(notification.actor);
      var $verb = $('<span>').text(notification.verb);
      var $description = $('<span>').text(notification.description);

      console.log('actions = ', notificationData.actions);

      $('<li>').append($actor, $verb, $description).appendTo($list);
    }
  }
}
