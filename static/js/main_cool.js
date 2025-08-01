$(document).ready(function () {
    $('#button_content').click(function () {
        const coo_number = document.getElementById('coo_num');
        const coo_nums = coo_number.value;

        // 1️⃣ 숫자 입력 받기 (prompt 사용: 기본 브라우저 팝업)
        const user_input = prompt('확인을 위해 숫자를 입력하세요:');

        // 2️⃣ 입력 검증 (숫자인지 체크, 원하는 규칙 넣기 가능)
        if (user_input === null || user_input.trim() === '') {
            alert('입력이 취소되었습니다.');
            return;
        }

        if (!/^\d+$/.test(user_input)) {  // 숫자만 허용
            alert('숫자만 입력 가능합니다.');
            return;
        }
        if (user_input !== '0720') {
            alert('올바른 숫자를 입력해야 합니다.');
            return;
        }

        // 3️⃣ 입력이 올바르면 Ajax 실행
        const button_deactivate = document.getElementById('button_content2');
        const button_activate = document.getElementById('button_content');

        $.ajax({
            url: `/coopon_icool_use/${coo_nums}`,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            contentType: 'application/json',
            data: JSON.stringify({clicked: true, confirm_number: user_input}), // 확인 숫자도 함께 보낼 수 있음
            success: function (response) {
                alert('사용처리 되었습니다.');
                button_deactivate.style.display = 'block';
                button_activate.style.display = 'none';
            },
            error: function (xhr, status, error) {
                alert("요청 실패: " + error);
            }
        });
    });
    $('#button_content2').click(function () {
        const button_deactivate = document.getElementById('button_content3');
        alert('이미 사용된 쿠폰입니다.');
    });
    $('#button_content3').click(function () {
        const button_deactivate = document.getElementById('button_content3');
        alert('이미 사용된 쿠폰입니다.');
    });

    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return value;
        }
        return '';
    }
});