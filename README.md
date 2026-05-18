# 🔒 CodeSentinel - AI代码安全卫士

<div align="center">

[![Stars](https://img.shields.io/github/stars/saya-ch/CodeSentinel?style=for-the-badge)](https://github.com/saya-ch/CodeSentinel/stargazers)
[![License](https://img.shields.io/github/license/saya-ch/CodeSentinel?style=for-the-badge)](LICENSE)
[![TRAE Skill](https://img.shields.io/badge/TRAE-Skill-blue?style=for-the-badge)](https://www.trae.ai/)
[![Last Commit](https://img.shields.io/github/last-commit/saya-ch/CodeSentinel?style=for-the-badge)](https://github.com/saya-ch/CodeSentinel/commits)

*A powerful AI code security auditing skill for TRAE SOLO*

</div>

---

## 📖 简介

**CodeSentinel** 是一款专门为检测AI生成代码安全漏洞而设计的智能审计Skill。它能自动识别常见的OWASP Top 10安全漏洞——SQL注入、XSS跨站脚本、硬编码凭证、命令注入等高危问题，并提供可操作的修复建议。

> 🤖 **AI帮你写代码，CodeSentinel帮你查漏洞**

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🛡️ **OWASP Top 10全覆盖** | 内置SQL注入、XSS、命令注入等主流漏洞检测规则 |
| 📊 **结构化报告** | 生成专业的安全审计报告，支持分享和存档 |
| 💡 **修复建议** | 每个漏洞都提供可运行的修复代码示例 |
| 🌐 **中文友好** | 全中文输出，国内开发者友好 |
| ⚡ **即时扫描** | 对话式即时扫描，无需复杂配置 |

---

## 🎯 适用人群

- 🔧 使用Copilot、Cursor等AI编程工具的开发者
- 👥 需要审核团队代码安全的Tech Lead  
- 💻 关注代码质量的后端/全栈工程师
- 🔒 担心AI代码引入漏洞的任何开发者

---

## 🐛 检测的漏洞类型

### 🔴 严重漏洞 (CVSS 9-10)

| 漏洞类型 | 检测模式 | CVSS |
|---------|---------|------|
| SQL注入 | `f"SELECT ... {user}"` | 9.8 |
| 命令注入 | `os.system(user_input)` | 9.1 |
| 硬编码凭证 | `API_KEY = "sk-..."` | 8.5 |
| 反序列化 | `pickle.loads(data)` | 8.1 |

### 🟠 高危漏洞 (CVSS 7-8.9)

| 漏洞类型 | 检测模式 | CVSS |
|---------|---------|------|
| XSS跨站脚本 | `innerHTML = user_input` | 8.1 |
| 路径遍历 | `open(path + user_file)` | 7.5 |

### 🟡 中危漏洞 (CVSS 4-6.9)

| 漏洞类型 | 检测模式 | CVSS |
|---------|---------|------|
| 弱密码哈希 | `hashlib.md5(password)` | 5.3 |
| 敏感信息泄露 | `print(password)` | 4.2 |

---

## 🚀 快速开始

### 方式一：在TRAE SOLO中导入

1. 下载 [`SKILL.md`](SKILL.md) 文件
2. 在TRAE中打开 **设置 → Rule & Skills**
3. 导入下载的Skill文件
4. 开始使用！

### 方式二：直接对话使用

```
用户：帮我用CodeSentinel扫描这段Python代码的安全漏洞

# 粘贴你的代码...
```

---

## 📖 使用示例

### 示例1：检测SQL注入

**被扫描代码：**
```python
def login(username, password):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
```

**CodeSentinel报告：**
```
┌─────────────────────────────────────────────────────────┐
│  🔍 CodeSentinel 安全审计报告                          │
├─────────────────────────────────────────────────────────┤
│  📊 漏洞统计                                            │
│  ├─ 🔴 严重：1                                         │
│  └─ 🟠 高危：0                                         │
└─────────────────────────────────────────────────────────┘

### [漏洞1] SQL注入 🔴 严重

**CVSS评分**：9.8 (严重)

**修复建议**：
```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```
```

### 示例2：检测硬编码凭证

**被扫描代码：**
```python
API_KEY = "sk-live-abc123xyz789"
SECRET = "my_secret_password"
```

**CodeSentinel报告：**
```
### [漏洞1] 硬编码凭证 🔴 严重

**修复建议**：
```python
import os
API_KEY = os.environ.get('API_KEY')
```
```

---

## 📁 仓库文件结构

```
CodeSentinel/
├── README.md              # 项目说明文档
├── SKILL.md               # TRAE SOLO Skill文件 ⭐
├── skill.json             # Skill元数据配置
├── system_prompt.md       # 系统提示词定义
├── demo/
│   ├── demo_vulnerable_code.py    # 有漏洞的演示代码
│   └── demo_security_report.md    # 扫描报告示例
├── docs/
│   ├── DETECTION_RULES.md         # 检测规则详解
│   ├── VULNERABILITY_GUIDE.md     # 漏洞知识库
│   └── REMEDIATION_GUIDE.md       # 修复指南
├── examples/
│   ├── python_vulnerabilities.py  # Python漏洞示例
│   └── js_vulnerabilities.js      # JavaScript漏洞示例
├── tests/
│   └── test_detection.py          # 单元测试
└── CONTRIBUTING.md                # 贡献指南
```

---

## 🔬 技术细节

### 检测引擎

- **静态分析**：基于AST和正则模式匹配
- **语义分析**：理解代码上下文，减少误报
- **多语言支持**：Python、JavaScript、TypeScript

### 评分标准

使用CVSS 3.1评分标准：
- 🔴 9.0-10.0: 严重
- 🟠 7.0-8.9: 高危
- 🟡 4.0-6.9: 中危
- 🟢 0.1-3.9: 低危

### 参考标准

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST SP 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/5/final)
- [Snyk Vulnerability Database](https://security.snyk.io/)

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

---

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 🙏 致谢

- [OWASP Foundation](https://owasp.org/) - 安全标准和教育资源
- [TRAE Team](https://www.trae.ai/) - AI编程平台
- 所有贡献者和用户

---

<div align="center">

**Made with ❤️ for developers who care about security**

⭐ Star us on GitHub | 🐛 Report a Bug | 📖 Read the Docs

</div>
