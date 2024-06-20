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
        "Password Is Not Valid "
    );
    // validation for email using regex
    $.validator.addMethod(
        "emailformat",
        function (value, element) {
        return (
            this.optional(element) ||
            /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/.test(
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
        "Mobile Number is not valid"
    );
    // validation for first name, last name
    $.validator.addMethod(
        "nameformat",
        function (value, element) {
        return (
            this.optional(element) ||
            /^[a-z[A-Z]+$/.test(value)
        );
        },
        "name is not valid"
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
                equalTo: "#id_password1"
            },
            email: {
                required: true,
                emailformat: true
            },
            first_name: {
                nameformat: true,
                required: true,
            },
            last_name: {
                nameformat: true,
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
                passwordformat: (
                        `password must be:
                        <li>8 Character long</li>
                        <li>contains one number and one special Character</li>`
                    )},
            password2:{
                required: "Please confirm Password",
                equalTo: "Password Does not match"
            },
            email: {
                required: "Please Enter Valid Email Address"
            },
            first_name: {
                nameformat: "first name is not valid",
                required: "Please Enter First Name",
            },
            last_name: {
                nameformat: "last name is not valid",
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