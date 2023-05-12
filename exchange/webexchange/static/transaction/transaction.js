window.onload = () => {
    const csrftoken = getCookie('csrftoken');
    const page_body_display = {
        zh: {
            "wallet-title": "钱包地址",
        },
        en: {
            "wallet-title": "Wallet Address",
        },
        kr: {
            "wallet-title": "지갑 주소",
        }
    }
    $('#language').on('change', (event) => {
        if (event.target.value === 'Chinese') {
            $('#coin').text(page_display_data.zh.nav.coin);
            $('#exchanges').text(page_display_data.zh.nav.exchanges);
            $('#swap').text(page_display_data.zh.nav.swap);
            $('#index').text(page_display_data.zh.nav.home);
            $("wallet-title").text()
        }
        else if (event.target.value === 'Korean') {
            $('#coin').text(page_display_data.kr.nav.coin);
            $('#exchanges').text(page_display_data.kr.nav.exchanges);
            $('#swap').text(page_display_data.kr.nav.swap);
            $('#index').text(page_display_data.kr.nav.home);
        }
        else {
            $('#coin').text(page_display_data.en.nav.coin);
            $('#exchanges').text(page_display_data.en.nav.exchanges);
            $('#swap').text(page_display_data.en.nav.swap);
            $('#index').text(page_display_data.en.nav.home);
        }
    });

    $('.wallet-heading').click(() => {
        $('.wallet-content').toggleClass('show');
    });
}