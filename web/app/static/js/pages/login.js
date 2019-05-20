$(document).ready(function(){
    clearFields(["#userLogin","#userPassword","#reg_user_name","#reg_user_login","#reg_user_password"])

    //clear fields on tab click
    $('#tab a[href="#signin"]').on('click', function (e) {
        e.preventDefault()
        clearFields(["#reg_user_name","#reg_user_login","#reg_user_password"])
        $(this).tab('show')
    });
    $('#tab a[href="#register"]').on('click', function (e) {
        e.preventDefault()
        clearFields(["#userLogin","#userPassword"])
        $(this).tab('show')
    });
});

function clearFields(fields){
    fields.forEach(function(element) {
        $(element).val("");
    });
}