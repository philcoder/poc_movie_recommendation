$(document).ready(function(){
    
    $.ajax({
        async: true,
        url: '/webui/userRatings',
        method: 'GET',
        success: function(serverData){
            // console.log(serverData)
            if(serverData.status === "ok"){
                history_table = $("#history_table").DataTable({
                    "searching": false,
                    "ordering": true,
                    "lengthChange": true,
                    "iDisplayLength": 7,
                    "aLengthMenu": [[7, 15, 30, 50, -1], [7, 15, 30, 50, "All"]],
                    data: serverData.history_ratings,
                    columns: [
                        {data: "title", "orderable": true},
                        {data: "rating", "orderable": true},
                        {data: "suggests", "orderable": true}
                    ]
                });
            }
        }
    })
});