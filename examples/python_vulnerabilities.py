#!/usr/bin/env python3
"""
CodeSentinel - 有漏洞的示例代码
用于演示Skill的安全检测能力
"""

# ========== 示例1: SQL注入漏洞 ==========

def vulnerable_user_login(username, password):
    """
    ❌ 有SQL注入漏洞的登录函数
    """
    import sqlite3

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # 🔴 SQL注入漏洞: 使用f-string字符串拼接
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()

    if result:
        return {"status": "success", "user": result}
    return {"status": "failed"}


# ========== 示例2: 硬编码凭证 ==========

def init_service():
    """
    ❌ 硬编码凭证的服务初始化
    """
    import os

    # 🔴 硬编码API密钥
    OPENAI_API_KEY = "sk-live-abc123xyz789"
    STRIPE_SECRET_KEY = "sk_live_abcdef123456"

    # 🔴 硬编码数据库密码
    DB_PASSWORD = "SuperSecret123!"

    # 🔴 硬编码JWT密钥
    JWT_SECRET = "my-super-secret-jwt-key"

    # 使用凭证
    os.environ["OPENAI_KEY"] = OPENAI_API_KEY

    return True


# ========== 示例3: 命令注入漏洞 ==========

def log_user_action(username, action):
    """
    ❌ 有命令注入漏洞的日志函数
    """
    import os
    import subprocess

    # 🔴 命令注入: 用户输入直接拼接到命令
    os.system(f"echo '[{username}] {action}' >> /var/log/app.log")

    # 🔴 命令注入: shell=True允许注入
    subprocess.call(f"echo 'User action logged' | mail -s 'Action' admin@example.com", shell=True)


# ========== 示例4: XSS漏洞 ==========

def render_user_comment(comment, username):
    """
    ❌ 有XSS漏洞的评论渲染
    """
    # 🔴 XSS漏洞: 未转义的用户输入直接插入HTML
    html = f"""
    <div class="comment">
        <span class="username">{username}</span>
        <div class="content">{comment}</div>
    </div>
    """
    return html


# ========== 示例5: 不安全反序列化 ==========

def load_user_preferences(user_id, pickled_data):
    """
    ❌ 有不安全反序列化漏洞
    """
    import pickle
    import base64

    # 🔴 反序列化漏洞: pickle可以执行任意代码
    data = base64.b64decode(pickled_data)
    preferences = pickle.loads(data)

    return preferences


# ========== 示例6: 路径遍历 ==========

def download_file(filename):
    """
    ❌ 有路径遍历漏洞的文件下载
    """
    import os

    # 🔴 路径遍历: 直接拼接用户输入
    file_path = "/app/uploads/" + filename

    # 没有验证路径是否在允许范围内
    with open(file_path, "rb") as f:
        content = f.read()

    return content


# ========== 示例7: 弱密码哈希 ==========

def hash_password(password):
    """
    ❌ 使用弱哈希算法的密码存储
    """
    import hashlib

    # 🔴 MD5已被破解，不应用于密码
    hashed = hashlib.md5(password.encode()).hexdigest()

    # 🔴 SHA1也已不安全
    hashed_sha1 = hashlib.sha1(password.encode()).hexdigest()

    return hashed


# ========== 示例8: 敏感信息泄露 ==========

def process_payment(card_number, cvv, amount):
    """
    ❌ 敏感信息泄露的支付处理
    """
    import logging

    # 🔴 敏感信息泄露: 打印到日志
    print(f"Payment processed - Card: {card_number}, CVV: {cvv}, Amount: ${amount}")

    # 🔴 敏感信息泄露: 日志记录
    logging.info(f"Processing payment: {card_number}")

    # 🔴 敏感信息泄露: 返回响应中包含完整信息
    return {
        "status": "success",
        "card": card_number,  # 不应在响应中返回完整卡号
        "message": "Payment processed successfully"
    }


# ========== 安全版本示例 ==========

def safe_login(username, password):
    """
    ✅ 安全版本的登录函数
    """
    import sqlite3

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # 使用参数化查询
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()
    conn.close()

    return {"status": "success" if result else "failed"}


def safe_hash_password(password):
    """
    ✅ 安全版本的密码哈希
    """
    import bcrypt

    # 使用bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)

    return hashed


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║        CodeSentinel 漏洞示例代码演示                   ║
    ╚══════════════════════════════════════════════════════════╝

    此文件包含多种常见的安全漏洞，用于演示CodeSentinel的检测能力：

    🔴 SQL注入         → login(), init_service()
    🔴 硬编码凭证      → init_service()
    🔴 命令注入        → log_user_action()
    🔴 XSS漏洞        → render_user_comment()
    🔴 不安全反序列化  → load_user_preferences()
    🔴 路径遍历       → download_file()
    🟡 弱密码哈希      → hash_password()
    🟡 敏感信息泄露    → process_payment()

    使用 CodeSentinel 扫描此文件即可发现所有漏洞！
    """)
