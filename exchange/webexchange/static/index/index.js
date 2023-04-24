window.onload = () => {
    const csrftoken = getCookie('csrftoken');
    $("#login").click((event) => {
        event.preventDefault();
        const data = {
            'click': 'login',
        }
        jumpTo(`/`, '/login/', data, csrftoken, 'POST');
    });
    $("#sign").click((event) => {
        event.preventDefault();
        const data = {
            'click': 'sign',
        }
        jumpTo(`/`, '/register/', data, csrftoken, 'POST');
    });
}