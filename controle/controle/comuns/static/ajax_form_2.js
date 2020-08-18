$(document).on("click", "#form", function() {

  $("#form").on("submit", function(event){
    event.preventDefault();
	var post_url = $(this).attr("action");
	var request_method = $(this).attr("method");
	var form_data = $(this).serialize();
	console.log(post_url, request_method, form_data)

    $.ajax({
      //headers: { "X-CSRFToken": $("#form").attr('data-token')},
        type: request_method,
        url: post_url,
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        },
        data: form_data,
        success: function(data,status){
        		console.log(data['stat'])
        		if(data['stat']=='OK'){ 
	      			window.location.reload();
	      		}
	      		else{
	      			document.getElementById("aviso").innerHTML = data;
	      		}
        },
        error: function(data){
          console.log(data);
          document.getElementById("aviso").innerHTML = data.responseJSON.error;  
        }
    });
})
  });

          // CSRF code
      function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (i; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }

      var csrftoken = getCookie('csrftoken');

      function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
      }
