
function searchMovie(){
    var data = {
        movie_name: $('#movie_search').val(),
    }

    $.ajax({
        async: true,
        url: '/webui/searchMovie',
        method: 'POST',
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        data: JSON.stringify(data),
        success: function(serverData){
            if(serverData.status === "ok"){
                populateMovieContent(serverData)
            }
        }
    })
}

function randomMovie(){
    $.ajax({
        async: true,
        url: '/webui/randomMovie',
        method: 'GET',
        success: function(serverData){
            //console.log(serverData)
            if(serverData.status === "ok"){
                populateMovieContent(serverData)
            }
        }
    })
}

function populateMovieContent(serverData){
    $('#movie_search').text("")
    $("#movie_title").text(serverData.movie.title);
    $("#movie_release").text(serverData.movie.release_date);
    $("#movie_genres").text(serverData.movie.genres);
    $('#movie_id').attr('value',serverData.movie.id);
    $("#movie_content").show();
}

function recommendationProcess(){
    var data = {
        movie_id: $('#movie_id').val(),
        rating: $('#movie_rating').val(),
    }

    $.ajax({
        async: true,
        url: '/webui/recommendation',
        method: 'POST',
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        data: JSON.stringify(data),
        success: function(serverData){
            //dispara uma consulta ao servidor a cada 5s para popular o proxima tabela
            console.log("recebido do servidor: "+serverData)
        }
    })
}