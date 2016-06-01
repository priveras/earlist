function vote(slug, direction, id) {
  $.post(slug + '/vote/' + direction + '/', {HTTP_X_REQUESTED:'XMLHttpRequest'},
      function(data){
        if(direction == 'up'){
          $('#votes-button-' + id).toggleClass('btn-default btn-primary');
        }
        else{
          $('#votes-button-' + id).toggleClass('btn-primary btn-default');
        }
        $('#votes-' + id).text(' ' + data);
      }
    )
  }

function status(slug, message, id) {
  $.post('status/' + slug + '/' + message + '/', {HTTP_X_REQUESTED:'XMLHttpRequest'},
      function(data){
        $('#status-button-' + id).toggleClass('btn-default btn-success');
        // if(direction == 'up'){
        //   $('#votes-button-' + id).toggleClass('btn-default btn-primary');
        // }
        // else{
        //   $('#votes-button-' + id).toggleClass('btn-primary btn-default');
        // }
        // $('#votes-' + id).text(' ' + data);
      }
    )
  }

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#upload').attr('class', 'fa fa-check-circle fa-lg m-l text-success');
    }
    reader.readAsDataURL(input.files[0]);
  }
}