$(document).ready(function() {
    $('#newsForm').submit(function(event) {
        event.preventDefault();

        var fromDate = $('#date_from').val();
        var toDate = $('#date_to').val();
        var sentiments = [];

        $('input[name="sentiment"]:checked').each(function() {
            sentiments.push($(this).val());
        });

        var preferences = {
            "fromDate": fromDate,
            "toDate": toDate,
            "sentiments": sentiments
        };
        console.log("Dev")
        console.log("THis is pre " ,preferences)
        $.ajax({
            type: 'POST',
            url: '/get_news',
            data: JSON.stringify({"preferences": preferences}),
            contentType: 'application/json',
            success: function(response) {
                
                console.log(response.news_links);
                
            }
        });
    });
});

