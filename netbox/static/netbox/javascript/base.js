$(document).on("click", "#btn-resource-list", function() {
  $('.resource-box').toggleClass('expanded');
  $('#btn-expand').toggleClass('hidden');
  $('#btn-collapse').toggleClass('hidden');
});

$(document).on("click", "#accept-cookies", function(e) {
  e.preventDefault();
  setCookie('accept-cookies', 1, 365);
  $('#cookies-notice').fadeOut(300);
});

$(document).on("click", "#user-signup", function(e) {
  ga('send', 'event', 'profile', 'signup');
});

$(document).on("click", "#user-email-confirm", function(e) {
  ga('send', 'event', 'profile', 'confirm');
});

$(document).ready(function() {
  $('[data-toggle="tooltip"]').tooltip();

  $('.more').shorten({
    'moreText': 'Read more',
    'showChars': 1500
  });
  $('.category-more').shorten({
    'moreText': 'Read more',
    'showChars': 500
  });

  // Show modal on profiles/edit page if user hasn't verified
  if (
    window.location.pathname === '/profiles/edit' &&
    $('body').data('userHasVerifiedEmail') === false
  ) {
    $('#verifyEmailModal').modal()
  }

  // Show modals for login or verification required when user clicks buttons
  // with data-requires-validated-user="true"
  $('[data-requires-validated-user]').on("click", function(e) {
    if ($('body').data('userIsAuthenticated') === false) {
      e.preventDefault();
      $('#loginRequiredModal').modal()
    }
    else if ($('body').data('userHasVerifiedEmail') === false) {
      e.preventDefault();
      $('#verifiedEmailRequiredModal').modal()
    }
  });

  // hide cookie notice, if user already accepted
  if (getCookie('accept-cookies')) {
    $('#cookies-notice').hide();
  }
});

function setCookie(name, value, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires=" + d.toUTCString();
  document.cookie = name + '=' + value + '; ' + expires + '; path=/';
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
