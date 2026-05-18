<!DOCTYPE html>
<html>
<head>
    <title>CodeSentinel - JavaScript漏洞示例</title>
</head>
<body>
    <h1>CodeSentinel - JS漏洞示例</h1>

    <!-- 示例1: XSS漏洞 -->
    <script>
        // ❌ XSS漏洞: innerHTML允许脚本注入
        function renderUserComment(comment) {
            document.getElementById('comments').innerHTML = comment;
        }

        // ❌ XSS漏洞: 用户输入直接写入文档
        function displayMessage(message) {
            document.write(`<div>${message}</div>`);
        }
    </script>

    <!-- 示例2: 敏感信息泄露 -->
    <script>
        // ❌ 敏感信息泄露: 控制台打印敏感数据
        function processLogin(username, password) {
            console.log(`Login attempt - User: ${username}, Pass: ${password}`);

            // ❌ 敏感信息泄露: 存储在localStorage
            localStorage.setItem('user_creds', JSON.stringify({
                username: username,
                password: password
            }));
        }
    </script>

    <!-- 示例3: 不安全的eval使用 -->
    <script>
        // ❌ 命令注入: eval可以执行任意代码
        function calculateExpression(expression) {
            return eval(expression);
        }

        // ❌ eval可以执行恶意代码
        function executeUserCode(code) {
            eval(code);
        }
    </script>

    <!-- 示例4: 路径遍历 -->
    <script>
        // ❌ 路径遍历: fetch API没有验证URL
        async function downloadFile(filename) {
            const response = await fetch(`/api/files/${filename}`);
            return response.text();
        }

        // ❌ 用户可以请求任意文件
        // 访问: downloadFile('../../../etc/passwd')
    </script>

    <!-- 示例5: 不安全的JWT处理 -->
    <script>
        // ❌ JWT不验证签名
        function parseJWT(token) {
            // 直接解码，不验证签名
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            return JSON.parse(window.atob(base64));
        }

        // ❌ 敏感数据存储在localStorage
        function saveToken(token) {
            localStorage.setItem('auth_token', token);
            localStorage.setItem('user_role', 'admin'); // 容易被篡改
        }
    </script>

    <!-- 安全版本 -->
    <script>
        // ✅ 安全: 使用textContent
        function safeRenderComment(comment) {
            document.getElementById('comment').textContent = comment;
        }

        // ✅ 安全: DOMPurify清理HTML
        function safeRenderHTML(html) {
            import('https://cdn.jsdelivr.net/npm/dompurify@3.0.0/dist/purify.min.js')
                .then(({ default: DOMPurify }) => {
                    const clean = DOMPurify.sanitize(html);
                    document.getElementById('content').innerHTML = clean;
                });
        }
    </script>
</body>
</html>
