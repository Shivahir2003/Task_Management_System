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
    "Password Is Not Valid"
  );
    $("#reset_password").validate({
        rules: {
            current_password: {
                passwordformat: true,
                required: true,
            },
            new_password: {
                passwordformat: true,
                required: true,
            },
            confirm_password: {
                required: true,
                equalTo:'#id_new_password'
            },
        },
        messages: {
            current_password: {
                required: "current_password is Required",
            },
            new_password: {
                required: "new_password is Required",
            },
            confirm_password: {
                required: "confirm_password is Required",
                equalTo: "Password Does not match",
            },

        },
        errorPlacement: function (error, element) {
            error.appendTo(element.next());
          },
    })
})