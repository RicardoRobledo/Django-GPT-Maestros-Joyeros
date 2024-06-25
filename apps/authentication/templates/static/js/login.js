$(document).ready(function() {
    $('body').fadeIn(1000);
});

$('#login').on('click', async function(event){
    event.preventDefault();

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const response = await fetch('https://django-gpt-maestros-joyeros.onrender.com/authentication/login/', {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            username: $('#username').val(),
            password: $('#password').val()
        })
    }).then(async (response) => {

        if (response.status === 302) {
            return response.json();
        }else{
            $('#message').show().delay(3000).fadeOut();
            throw new Error('Request failed with status');
        }
    
    }).then(async (data) => {

        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('code', data['code']);
        window.location.href = data['callback_url']+'?'+urlParams.toString();
        
        return data;
    
    }).catch(error => {
        console.error('Error:', error);
    });

})
