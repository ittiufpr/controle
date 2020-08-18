$(document).on("click", "#form", function() {

  $("#form").on("submit", function(){
    event.preventDefault();
    $.ajax({
      //headers: { "X-CSRFToken": $("#form").attr('data-token')},
      type: "POST",
        url: $("#form").attr('action'),
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        },
        //url: "",
        //data: ("#form").serialize,
        success: function(data,status){
            console.log(status);
            //document.getElementById("aviso").innerHTML = "<h2 style='text-align:center;background-color:green;'>SUCCESS</h2>";
            document.getElementById("aviso").innerHTML = data;  
      window.location.reload();

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