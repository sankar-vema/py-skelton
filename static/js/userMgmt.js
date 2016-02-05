$(document).ready(function(){
  $('#usertable').DataTable();

  $('#addNewUser').click(function(){
    $('.overlay-bg, .popup').show();
  });

  $('.remove').click(function(){
    $('.overlay-bg, .overlay-content').hide();  
  });

  /*function validateEmail($email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return emailReg.test( $email );
  }

  $('.overlay-content.popup #addUser').click(function(){
    var username = $('#username').val().length,
        firstname = $('#firstname').val().length,
        lastname = $('#lastname').val().length,
        email = $('#email').val().length;

    if(username != '' || firstname != '' || lastname != '' || email != ''){
      $('form[name="addUserForm"]').submit();
    }else{
      return false;
    }
  });*/


  $("#userdataform").validate({
    rules: {
      username: "required",
      firstname: "required",
      lastname: "required",
      email: {
        required: true,
        email: true
      }
    },
    messages: {
      username: "Please specify Short ID",
      firstname: "Please specify Firstname",
      lastname: "Please specify Lastname",
      email: {
        required: "Please specify Email",
        email: "Your email address must be in the format of name@domain.com"
      }
    },
    submitHandler: function(form) {
      $('form[name="addUserForm"]').submit();
    }
  });
});

