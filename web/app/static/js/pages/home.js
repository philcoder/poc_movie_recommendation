
function executeProcess(){
    var data = {
        type: "movie",
        tags: "adventure"
    }

    $.ajax({
        async: true,
        url: '/webui/recommendation',
        method: 'POST',
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        data: JSON.stringify(data),
        success: function(serverData){
            console.log("recebido do servidor: "+serverData)
        }
    })
}