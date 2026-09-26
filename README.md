# spain-student-hub
西班牙留学生一站式工具站
# 🇪🇸 西班牙留学生一站式工具站

一个专为在西班牙的中国留学生打造的免费在线工具集。支持中文、英文、西班牙语，帮助留学生更高效地学习、生活和交流。

## 🔗 在线使用地址

**[👉 点此打开工具站](https://your-spain-student-tools.streamlit.app)**

（把上面的链接替换成你自己的 Streamlit 应用网址）

## ✨ 功能列表

### 1. 🔍 AI 文本检测器
- 粘贴一段文字，判断它是人类写的还是 AI 生成的
- 基于数学统计法（句子波动性 + 词汇多样性），不依赖外部模型，秒级出结果
- 支持中文、英文、西班牙语
- 内测用户的个性化经验库：专门针对中国留学生的“中式西语”问题给出修改建议
- **登录用户可以使用检测历史记录、收藏等功能**

### 2. 🌐 简易翻译器
- 支持中文、英文、西班牙语互译
- 简洁直观的界面，适合日常学习和生活场景

### 3. 👤 用户系统
- 支持 Google 账号一键登录
- 登录后可保存检测历史、设置个性化昵称和 Emoji 头像
- 免费用户可用基础功能，未来将推出会员增值服务

## 🛠️ 技术栈

- **前端/后端框架**：[Streamlit](https://streamlit.io/)
- **数据库**：[Supabase](https://supabase.com/)（PostgreSQL）
- **用户认证**：Streamlit 原生 Google OAuth 登录
- **开发语言**：Python

## 🚀 本地运行

如果你想在本地跑起来：

1. 克隆仓库：
   ```bash
   git clone https://github.com/pseebat0312-gif/spain-student-hub.git
   cd spain-student-hub
