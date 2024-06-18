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
    // validation for email using regex
    $.validator.addMethod(
        "emailformat",
        function (value, element) {
        return (
            this.optional(element) ||
            /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(
            value
            )
        );
        },
        "Email Address is Not Valid"
    );
    // validation for Moblie number using regex
    $.validator.addMethod(
        "numberformat",
        function (value, element) {
        return (
            this.optional(element) ||
            /^[0-9]*$/.test(
            value
            )
        );
        },
        "Mobile Number Has no Alphabets"
    );

    $("#signup").validate({
        rules:{
            username: {
                required: true
            },
            password1: {
                required: true,
                minlength: 8,
                passwordformat: true,
            },
            password2:{
                required: true,
                minlength: 8,
            },
            email: {
                required: true,
                emailformat: true
            },
            first_name: {
                required: true,
            },
            last_name: {
                required: true,
            },
            mobile_number: {
                required: true,
                maxlength: 10,
                numberformat: true
            }
        },
        messages: {
            username:{
                required: "Please Enter Username",
            },
            password1: {
                required: "Please Enter Password",
                minlength: "Minimum Length Is 8 "

            },
            password2:{
                required: "Please Confirm Your Password",
            },
            email: {
                required: "Please Enter Valid Email Address"
            },
            first_name: {
                required: "Please Enter First Name",
            },
            last_name: {
                required: "Please Enter Your Last Name",
            },
            mobile_number: {
                required: "Please Enter Mobile Number",
                maxlength: "Moblie Number Must Be 10 Digits"
            }

        },
        errorPlacement: function (error, element) {
            error.appendTo(element.next());
          },
    })
})