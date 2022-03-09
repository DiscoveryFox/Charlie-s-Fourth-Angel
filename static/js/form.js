$(document).ready(function () {

    $('#ngrok_ip_get').on('submit', function (event) {
        $.ajax({
            data: {
                service: $('#port_forwarding').val(),
                template: $('#template').val()
            },
            type: 'POST',
            url: '/get_link'
        })
            .done(function (data) {
                $('#ngrok_url').text(data).show();
                $('#stop_camphish').toggle();
            });

        event.preventDefault();
    });
});