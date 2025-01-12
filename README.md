# AI Glasses Agent
# AI智能眼镜项目

A web-based platform for AI-powered smart glasses applications, featuring real-time translation, health tracking, and navigation assistance.
基于网络的AI智能眼镜应用平台，提供实时翻译、健康追踪和导航辅助功能。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](#english) | [中文](#chinese)

<a name="english"></a>
## Overview
AI Glasses Agent is an innovative open-source project that combines cutting-edge AI technology with smart glasses hardware to create practical, everyday applications. Our platform provides a suite of AI-powered features designed to enhance accessibility, education, and health monitoring.

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-glasses-agent.git
cd ai-glasses-agent

# Frontend setup
cd frontend/ai-glasses-frontend
npm install
npm run dev

# Backend setup
cd backend/ai-glasses-agent-backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Features

### 1. Educational Translation Assistant
- Real-time translation of objects and text through smart glasses
- Point-and-translate functionality for seamless learning experience
- Support for multiple languages

### 2. Health & Calorie Tracking
- Automatic food recognition and calorie tracking
- Personal database for meal history
- Nutritional information display

### 3. Navigation Assistant for Visually Impaired
- Real-time environment description
- Obstacle detection and warning system
- Voice-based navigation guidance

## Project Structure
```
ai-glasses-agent/
├── frontend/          # React-based web interface
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/        # Page components
│   │   └── context/      # React context providers
│   └── public/
└── backend/           # FastAPI backend server
    ├── app/
    │   ├── models.py     # Data models
    │   └── database.py   # Database operations
    └── tests/
```

## Technology Stack
- Frontend: React with TypeScript, Tailwind CSS
- Backend: FastAPI (Python)
- Database: In-memory database for prototype
- Languages: Multi-language support (EN, ZH, ES, FR, DE, JA, KO)

## 🔧 Secondary Development Guide
Want to build your own features on top of this project? Here's how:

### Prerequisites Explained
1. **Node.js** (16+)
   - What it does: Runs JavaScript code outside the browser
   - Why we need it: Powers our frontend development
   - Install from: https://nodejs.org/

2. **Python** (3.8+)
   - What it does: Programming language for backend
   - Why we need it: Powers our API and AI features
   - Install from: https://python.org/

3. **Git**
   - What it does: Tracks code changes
   - Why we need it: Helps manage code versions
   - Install from: https://git-scm.com/

### Adding New Features

1. **Frontend Development**
   ```bash
   # Example: Adding a new page
   cd frontend/ai-glasses-frontend
   
   # Create new page component
   touch src/pages/NewFeaturePage.tsx
   
   # Add route in App.tsx
   # Add to src/App.tsx:
   # <Route path="/new-feature" element={<NewFeaturePage />} />
   ```

2. **Backend Development**
   ```bash
   # Example: Adding new API endpoint
   cd backend/ai-glasses-agent-backend
   
   # Add endpoint in app/main.py:
   # @app.post("/api/new-feature")
   # async def new_feature():
   #     return {"message": "New feature works!"}
   ```

3. **Database Changes**
   ```python
   # Add new model in app/models.py
   class NewFeature(BaseModel):
       name: str
       description: str
   
   # Add to database.py
   def add_new_feature(self, feature: NewFeature):
       # Implementation here
       pass
   ```

### Common Development Scenarios

1. **Modifying UI Components**
   - Location: `frontend/src/components/`
   - Example: Changing ApplicationCard style
   ```tsx
   // Edit src/components/ApplicationCard.tsx
   export function ApplicationCard({ title, description }) {
     return (
       <div className="your-custom-styles">
         {/* Your modifications */}
       </div>
     )
   }
   ```

2. **Adding Language Support**
   - Modify: `src/context/LanguageContext.tsx`
   - Add translations to relevant components

3. **Extending AI Features**
   - Location: `backend/app/main.py`
   - Add new AI model integration
   - Implement new processing endpoints

### 🐛 Troubleshooting Common Issues

1. **Node.js Errors**
   ```bash
   # Clear node_modules and reinstall
   rm -rf node_modules
   npm install
   ```

2. **Python Environment Issues**
   ```bash
   # Recreate virtual environment
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Git Problems**
   ```bash
   # Reset local changes
   git fetch origin
   git reset --hard origin/main
   ```

## Contributing
We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for guidelines.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Commercial Applications
- Educational institutions for language learning programs
- Healthcare facilities for dietary monitoring
- Assistive technology providers for vision assistance solutions
- Smart glasses manufacturers for feature integration

## Community & Support
- Report issues and feature requests on GitHub
- Join our discussions for ideas and feedback
- Follow our development progress
- Need help? Email: support@ai-glasses-agent.com

---

<a name="chinese"></a>
# 中文文档

## 概述
AI智能眼镜是一个创新的开源项目，将尖端AI技术与智能眼镜硬件相结合，创造实用的日常应用。我们的平台提供一系列AI驱动的功能，旨在提升无障碍性、教育和健康监测。

### 快速开始
```bash
# 克隆仓库
git clone https://github.com/yourusername/ai-glasses-agent.git
cd ai-glasses-agent

# 前端设置
cd frontend/ai-glasses-frontend
npm install
npm run dev

# 后端设置
cd backend/ai-glasses-agent-backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 功能特点
### 1. 教育翻译助手
- 通过智能眼镜实时翻译物体和文本
- 指点即译功能，实现无缝学习体验
- 支持多种语言

### 2. 健康和卡路里追踪
- 自动食物识别和卡路里追踪
- 个人餐饮历史数据库
- 营养信息显示

### 3. 视障人士导航助手
- 实时环境描述
- 障碍物检测和警告系统
- 基于语音的导航指引

## 项目结构
```
ai-glasses-agent/
├── frontend/          # React前端界面
│   ├── src/
│   │   ├── components/    # 可复用UI组件
│   │   ├── pages/        # 页面组件
│   │   └── context/      # React上下文提供者
│   └── public/
└── backend/           # FastAPI后端服务器
    ├── app/
    │   ├── models.py     # 数据模型
    │   └── database.py   # 数据库操作
    └── tests/
```

## 技术栈
- 前端：React with TypeScript, Tailwind CSS
- 后端：FastAPI (Python)
- 数据库：原型阶段使用内存数据库
- 语言：多语言支持（英语、中文、西班牙语、法语、德语、日语、韩语）

## 参与贡献
我们欢迎开发者、设计师和AI爱好者的贡献！请阅读我们的[贡献指南](CONTRIBUTING.md)了解如何参与。

## 许可证
本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## 商业应用
- 教育机构的语言学习项目
- 医疗机构的饮食监测
- 视觉辅助技术提供商的解决方案
- 智能眼镜制造商的功能集成

## 🔧 二次开发指南
想要在这个项目的基础上开发自己的功能？以下是详细步骤：

### 前置工具说明
1. **Node.js** (16+)
   - 作用：在浏览器外运行JavaScript代码
   - 为什么需要：驱动前端开发
   - 下载地址：https://nodejs.org/

2. **Python** (3.8+)
   - 作用：后端编程语言
   - 为什么需要：支持API和AI功能
   - 下载地址：https://python.org/

3. **Git**
   - 作用：跟踪代码变更
   - 为什么需要：帮助管理代码版本
   - 下载地址：https://git-scm.com/

### 添加新功能

1. **前端开发**
   ```bash
   # 示例：添加新页面
   cd frontend/ai-glasses-frontend
   
   # 创建新页面组件
   touch src/pages/NewFeaturePage.tsx
   
   # 在App.tsx中添加路由
   # 添加到src/App.tsx:
   # <Route path="/new-feature" element={<NewFeaturePage />} />
   ```

2. **后端开发**
   ```bash
   # 示例：添加新API端点
   cd backend/ai-glasses-agent-backend
   
   # 在app/main.py中添加端点:
   # @app.post("/api/new-feature")
   # async def new_feature():
   #     return {"message": "新功能正常工作！"}
   ```

3. **数据库修改**
   ```python
   # 在app/models.py中添加新模型
   class NewFeature(BaseModel):
       name: str
       description: str
   
   # 在database.py中添加
   def add_new_feature(self, feature: NewFeature):
       # 实现代码
       pass
   ```

### 常见开发场景

1. **修改UI组件**
   - 位置：`frontend/src/components/`
   - 示例：修改ApplicationCard样式
   ```tsx
   // 编辑 src/components/ApplicationCard.tsx
   export function ApplicationCard({ title, description }) {
     return (
       <div className="你的自定义样式">
         {/* 你的修改 */}
       </div>
     )
   }
   ```

2. **添加语言支持**
   - 修改：`src/context/LanguageContext.tsx`
   - 在相关组件中添加翻译

3. **扩展AI功能**
   - 位置：`backend/app/main.py`
   - 添加新的AI模型集成
   - 实现新的处理端点

### 🐛 常见问题解决

1. **Node.js错误**
   ```bash
   # 清理node_modules并重新安装
   rm -rf node_modules
   npm install
   ```

2. **Python环境问题**
   ```bash
   # 重新创建虚拟环境
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Git问题**
   ```bash
   # 重置本地更改
   git fetch origin
   git reset --hard origin/main
   ```

## 社区与支持
- 在GitHub上报告问题和功能请求
- 加入我们的讨论，分享想法和反馈
- 关注我们的开发进展
- 需要帮助？邮箱：support@ai-glasses-agent.com
