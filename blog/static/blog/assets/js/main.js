function vote(slug, direction, id) {
  $.post(slug + '/vote/' + direction, {HTTP_X_REQUESTED:'XMLHttpRequest'},
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