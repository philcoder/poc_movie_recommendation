
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
            }else{
                $('#movie_search_error').html("Movie didn't found in database")
                $('#movie_search').addClass("is-invalid")
                $("#movie_content").hide();
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
            if(serverData.status === "ok"){
                populateMovieContent(serverData)
            }
        }
    })
}

function populateMovieContent(serverData){
    $('#movie_search').val("")
    $('#movie_search').removeClass("is-invalid")

    $("#movie_title").text(serverData.movie.title);
    $("#movie_release").text(serverData.movie.release_date);
    $("#movie_genres").text(serverData.movie.genres);
    $('#movie_id').attr('value',serverData.movie.id);
    $("#movie_content").show();
}

function disableButtons(){
    $("#btn_recommendation").attr("disabled", true);
    $("#btn_recommendation").html(
        `<span class="spinner-border spinner-border-sm"></span>   Recommendation Movie`
    );
    $("#btn_search_movie").attr("disabled", true);
    $("#btn_random_movie").attr("disabled", true);
}

function enableButtons(){
    $("#btn_recommendation").attr("disabled", false);
    $("#btn_recommendation").empty();
    $("#btn_search_movie").attr("disabled", false);
    $("#btn_random_movie").attr("disabled", false);
}

function recommendationProcess(){
    $("#movie_top5_content").hide();
    disableButtons()


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
            if(serverData.status === "ok"){
                var watchCount = 1
                var watchInterval = setInterval(function(){
                    $.ajax({
                        async: true,
                        url: '/webui/watchRecommendation',
                        method: 'POST',
                        contentType: "application/json; charset=utf-8",
                        dataType: 'json',
                        data: JSON.stringify({rating_id : serverData.rating_id}),
                        success: function(watchServerData){
                            if(watchServerData.status === "ok"){
                                stopInterval()
                                populateMovieTop5Content(watchServerData)

                            }else{
                                if(watchCount == 5){
                                    stopInterval()
                                }
                            }
                            watchCount += 1
                        }
                    })
                }, 3000);

                var stopInterval = function () {
                    clearInterval(watchInterval)
                    enableButtons()
                };
            }else{

            }
        }
    })
}

function populateMovieTop5Content(serverData){
    $("#movie_top5").empty();
    $("#btn_recommendation").html(
        `Recommendation Movie`
    );
    serverData.movies.forEach(function(elem){
        text = []
        text.push("<li>")
        text.push("<b>"+elem.title + "</b>; "+elem.genres)
        text.push("</li>")
        $("#movie_top5").append(text.join(""));
    })
    $("#movie_top5_content").show();
}