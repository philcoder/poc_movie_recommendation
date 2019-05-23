
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
    $("#movie_title").text(serverData.movies.title);
    $("#movie_release").text(serverData.movies.release_date);
    $("#movie_genres").text(serverData.movies.genres);
    $("#movie_content").show();
}








function recommendationProcess(){
    var data = {
        type: "movie",
        tags: ["action", "adventure"]
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