document.addEventListener('DOMContentLoaded', function() {
    // 初始化flag状态
    document.body.dataset.flag = true;

    window.mySwitch = function() {
        let flag = JSON.parse(document.body.dataset.flag); // 使用data属性存储flag状态

        if (flag) {
            // 切换到登录表单
            
            $(".login-form").show(); // 显示登录表单
            $(".pre-box").css({
                "transform": "translateX(100%)", // 修改为原始位置或其他效果
                "background-color": "rgb(244, 208, 0)"
            });
           
        } else {
            // 切换到注册表单
            $(".register-form").show(); // 显示注册表单
            $(".pre-box").css({
                "transform": "translateX(0%)", // 修改为原始位置或效果
                "background-color": "rgb(213, 23, 0)"
            });
            $(".img-box img").attr("src", "../static/post_picture.jpg");
        }

        var registerForm = document.querySelector('.register-form');
        var loginForm = document.querySelector('.login-form');
        
        document.body.dataset.flag = !flag; // 切换flag的状态
    };
    
    // 登录按钮点击事件
    document.getElementById('login-btn').addEventListener('click', function () {
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        // 表单验证
        if (!username || !password) {
            alert('请填写用户名和密码！');
            return;
        } else {
            window.location.href = ''; // 替换为目标页面的 URL
        }

    });
});