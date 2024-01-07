$(document).ready(function() {
    $('#mvp-vote-form').submit(function(e) {
        e.preventDefault();
        var player_id = $('select[name="player_id"]').val();
        $.ajax({
            url: '/vote_for_mvp/',
            type: 'post',
            data: { 'player_id': player_id },
            success: function(data) {
                $('#vote-results').html('Thank you for voting. MVP vote recorded.');
            },
            error: function(error) {
                console.log(error);
                $('#vote-results').html('Error occurred while voting.');
            }
        });
    });
});
