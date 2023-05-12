
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function jumpTo(curr_page, dest_page, data, csrftoken, method) {
    fetch(curr_page, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    }).then(response => {
        window.location.href = dest_page;
    });
};

const page_display_data = {
    "zh": {
        nav: {
            coin: "货币",
            exchanges: "交易",
            swap: "兑换",
            home: "主页",
        },
        contents: {
            user: "用户",
            password: "密码"
        },
        button: {
            login: "登录",
            register: "注册",
            cancel: "取消"
        }
    },
    "kr": {
        nav: {
            coin: '코인',
            exchanges: '거래소',
            swap: '교환',
            home: '홈'
        },
        contents: {
            user: "계정",
            password: "비밀번호"
        },
        button: {
            login: '로그인',
            register: '회원가입',
            cancel: '취소'
        }
    },
    "en": {

        nav: {
            coin: 'Coins',
            exchanges: 'Exchanges',
            swap: 'Swap',
            home: 'Home'
        },
        contents: {
            user: "User",
            password: "Password"
        },
        button: {
            login: "Login",
            register: "Register",
            cancel: "Cancel"
        }
    }
}