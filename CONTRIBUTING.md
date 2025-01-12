# Contributing to AI Glasses Agent
# AI智能眼镜项目贡献指南

Thank you for your interest in contributing to AI Glasses Agent!
感谢您有兴趣为AI智能眼镜项目做出贡献！

## Getting Started 开始使用

### Prerequisites 前置要求
- Node.js 16+ and npm
- Python 3.8+
- Git

### Development Setup 开发环境设置
1. Clone the repository 克隆仓库
```bash
git clone https://github.com/yourusername/ai-glasses-agent.git
cd ai-glasses-agent
```

2. Frontend Setup 前端设置
```bash
cd frontend/ai-glasses-frontend
npm install
npm run dev
```

3. Backend Setup 后端设置
```bash
cd backend/ai-glasses-agent-backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Development Guidelines 开发指南

### Code Style 代码风格
- Frontend: Follow TypeScript and React best practices
- Backend: Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add comments for complex logic

前端：遵循TypeScript和React最佳实践
后端：遵循PEP 8规范
使用有意义的变量和函数名
为复杂逻辑添加注释

### Pull Request Process Pull Request流程
1. Fork the repository 复刻仓库
2. Create a feature branch 创建功能分支
3. Commit your changes 提交更改
4. Push to your fork 推送到您的仓库
5. Submit a Pull Request 提交Pull Request

### Commit Messages 提交信息
Format 格式:
```
type(scope): description

[optional body]
```

Types 类型:
- feat: New feature 新功能
- fix: Bug fix 修复
- docs: Documentation 文档
- style: Code style 代码风格
- refactor: Code refactoring 重构
- test: Testing 测试
- chore: Build/maintenance 构建/维护

### Testing 测试
- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Follow test naming conventions

为新功能编写单元测试
确保所有测试通过后再提交PR
遵循测试命名规范

## Project Structure 项目结构
```
ai-glasses-agent/
├── frontend/          # React frontend 前端
│   ├── src/
│   ├── public/
│   └── package.json
└── backend/           # FastAPI backend 后端
    ├── app/
    ├── tests/
    └── requirements.txt
```

## Need Help? 需要帮助？
- Open an issue 提出问题
- Join our community discussions 加入社区讨论
- Read our documentation 阅读文档

## License 许可
By contributing, you agree that your contributions will be licensed under the MIT License.
通过贡献，您同意您的贡献将在MIT许可下发布。
