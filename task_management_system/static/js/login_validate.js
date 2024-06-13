$(document).ready(function(){

    // validation for password
  $.validator.addMethod(
    "passwordformat",
    function (value, element) {
      return (
        this.optional(element) ||
        /^(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$/.test(value)
      );
    },
    "password is not valid"
  );

  $('#login').validate({
    rules: {
        username: {
            required: true,
        },
        password : {
            passwordformat: true,
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