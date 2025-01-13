# Image2Video Plugin for ChatGPT-on-WeChat

将图片转换为视频的插件，支持自定义动画效果。

## 系统要求

- Python >= 3.8
- ChatGPT-on-WeChat 最新版本
- 稳定的网络连接
- 足够的磁盘空间用于临时文件

## 功能特点

- 支持上传图片并转换为视频
- 自定义动画效果描述
- 支持多种图片格式
- 提供详细的处理状态反馈
- 自动清理临时文件

## 本地安装测试步骤

1. 准备环境：
   ```bash
   # 创建并激活虚拟环境（推荐）
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   .\venv\Scripts\activate  # Windows
   ```

2. 安装依赖：
   ```bash
   cd /path/to/chatgpt-on-wechat
   pip install -r plugins/image2video/requirements.txt
   ```

3. 配置插件：
   - 复制配置文件：
     ```bash
     cp plugins/image2video/config.json.example plugins/image2video/config.json
     ```
   - 编辑 config.json 填入必要信息：
     - `api_url`: API服务器地址
     - `imgbb_api_key`: ImgBB API密钥（用于图片上传）
     - `ak`: API访问密钥
     - `sk`: API密钥

4. 启动测试：
   ```bash
   python app.py
   ```

## 使用方法

1. 发送 "动起来" 启动视频生成流程
2. 在3分钟内上传需要处理的图片
3. 输入期望的动画效果描述
4. 等待视频生成完成（约10-18分钟）

## 本地测试验证

1. 验证安装：
   - 检查插件是否正确加载（查看启动日志）
   - 确认配置文件是否被正确读取
   - 验证临时文件目录是否可写

2. 功能测试：
   - 发送 "动起来" 命令，确认收到回复
   - 上传测试图片，验证上传功能
   - 输入动画描述，检查任务提交
   - 等待并确认最终视频生成

3. 常见问题排查：
   - 图片上传失败：
     * 检查网络连接
     * 验证 imgbb_api_key 是否有效
     * 确认图片格式支持
   - 视频生成失败：
     * 检查 ak/sk 配置
     * 确认 API 服务可访问
     * 查看错误日志详情

## 注意事项

- 确保图片清晰可用
- 动画效果描述越详细越好
- 处理时间可能较长，请耐心等待
- 建议先用小图片测试功能
- 保持网络稳定连接

## 错误处理

如遇到问题，请按以下步骤排查：

1. 检查日志输出：
   ```bash
   tail -f chatgpt.log
   ```

2. 验证配置：
   ```bash
   python -c "import json; json.load(open('plugins/image2video/config.json'))"
   ```

3. 测试网络连接：
   ```bash
   curl -I https://api.klingai.com/v1/videos/image2video
   ```

4. 如果问题持续，请：
   - 检查 Python 版本兼容性
   - 确认所有依赖都已安装
   - 验证文件权限设置
   - 查看系统资源使用情况
