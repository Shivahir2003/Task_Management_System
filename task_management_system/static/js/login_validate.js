$(document).ready(function(){

  $('#login').validate({
    rules: {
        username: {
            required: true,
        },
        password : {
            required: true,
        }
    },
    messages: {
        username: {
            required: "username is required",
        },
        password:{
            required: "Password is required",
        }
    },
    errorPlacement: function (error, element) {
        error.appendTo(element.next());
      },
  })
})