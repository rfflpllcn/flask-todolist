$(document).ready(function() {
  $(':checkbox').on('click', changeIdeaStatus);
});

function changeIdeaStatus() {
  if ($(this).is(':checked')) {
    putNewStatus($(this).data('idea-id'), true);
  } else {
    putNewStatus($(this).data('idea-id'), false);
  }
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// function from the django docs
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1)
        );
        break;
      }
    }
  }
  return cookieValue;
}

function putNewStatus(ideaID, isFinished) {

  // setup ajax to csrf token
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  // send put request using the todo of the get for the same id
  var ideaURL = '/api/idea/' + ideaID + '/'
  $.getJSON(ideaURL, function(idea) {
    idea.is_finished = isFinished;
    $.ajax({
      url: ideaURL,
      type: 'PUT',
      contentType: 'application/json',
      data: JSON.stringify(idea),
      success: function() {
        location.reload();
      }
    });
  });
}
