window.onload = () => {

    const csrftoken = getCookie('csrftoken');
    $("#submit").click((event) => {
        event.preventDefault();        // prevent to jump a new page
        const data = {
            click: 'submit',
            'username': $('#username').val(),
            'userpassword': $('#userpassword').val(),
        };
        jumpTo(`/login/`, '/coins/', data, csrftoken, 'POST');
    });
    // request to login backend code and response is OK to jump a new page
    $("#cancel").click((event) => {
        event.preventDefault();
        const data = {
            'click': 'cancel',
        }
        jumpTo(`/login/`, '/', data, csrftoken, 'POST');
    });
    $("#register").click((event) => {
        event.preventDefault();
        const data = {
            'click': 'register',
        }
        jumpTo(`/login/`, '/register/', data, csrftoken, 'POST');
    });
    $('#language').on('change', (event) => {
        if (event.target.value === 'Chinese') {
            // nav
            $('#coin').text(page_display_data.zh.nav.coin);
            $('#exchanges').text(page_display_data.zh.nav.exchanges);
            $('#swap').text(page_display_data.zh.nav.swap);
            $('#index').text(page_display_data.zh.nav.home);
            // others
            $("#user-title").text(page_display_data.zh.contents.user);
            $("#password-title").text(page_display_data.zh.contents.password);
            $("#submit").text(page_display_data.zh.button.login);
            $("#register").text(page_display_data.zh.button.register);
            $("#cancel").text(page_display_data.zh.button.cancel);
        }
        else if (event.target.value === 'Korean') {
            // nav
            $('#coin').text(page_display_data.kr.nav.coin);
            $('#exchanges').text(page_display_data.kr.nav.exchanges);
            $('#swap').text(page_display_data.kr.nav.swap);
            $('#index').text(page_display_data.kr.nav.home);
            // others
            $("#user-title").text(page_display_data.kr.contents.user);
            $("#password-title").text(page_display_data.kr.contents.password);
            $("#submit").text(page_display_data.kr.button.login);
            $("#register").text(page_display_data.kr.button.register);
            $("#cancel").text(page_display_data.kr.button.cancel);
        }
        else {
            // nav
            $('#coin').text(page_display_data.en.nav.coin);
            $('#exchanges').text(page_display_data.en.nav.exchanges);
            $('#swap').text(page_display_data.en.nav.swap);
            $('#index').text(page_display_data.en.nav.home);
            // others
            $("#user-title").text(page_display_data.en.contents.user);
            $("#password-title").text(page_display_data.en.contents.password);
            $("#submit").text(page_display_data.en.button.login);
            $("#register").text(page_display_data.en.button.register);
            $("#cancel").text(page_display_data.en.button.cancel);
        }
    });
}