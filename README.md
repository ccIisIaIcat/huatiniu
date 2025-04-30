# 话题牛 (HuaTiNiu)

一个自动化内容生产和发布的工具集，用于高效地生成、处理和发布多平台内容。

## 项目依赖

### 必需的外部服务
1. **Fish Speech**
   - 需要在本地部署 Fish Speech 服务
   - 确保服务正常运行并可访问

2. **OpenAI API**
   - 需要有效的 OpenAI API Key
   - 用于内容生成和处理

## 项目结构

- `bilibili/`: B站内容上传和管理模块
- `check/`: 内容检查和验证模块
- `cutmovie/`: 视频处理和剪辑模块
- `introduction/`: 项目介绍和演示模块
- `ppt/`: 演示文稿相关资源
- `tts/`: 文本转语音处理模块
- `zhihu/`: 知乎内容管理模块
- `SOP/`: 标准操作流程文档

## 主要功能

1. **内容发现和生成**
   - 自动化话题发现
   - AI辅助内容生成
   - 多样化内容模板

2. **视频处理**
   - 视频剪辑和合成
   - 背景音乐添加
   - 视频加速处理

3. **音频处理**
   - 文本转语音（TTS）
   - 音频速度调整
   - 音频格式转换

4. **多平台发布**
   - B站自动发布
   - 知乎内容管理
   - 跨平台内容分发

## 配置说明

1. **API密钥配置**
   ```
   # 在项目根目录创建 .env 文件
   OPENAI_API_KEY=your_api_key_here
   ```

2. **Fish Speech 配置**
   - 确保Fish Speech服务在本地运行
   - 默认访问地址：`http://localhost:YOUR_PORT`

## 使用流程

1. 配置环境
   ```bash
   # 安装依赖
   pip install -r requirements.txt
   
   # 配置API密钥
   # 启动Fish Speech服务
   ```

2. 运行内容生成
   ```bash
   python tts/master.py  # 运行TTS处理
   python cutmovie/master.py  # 运行视频处理
   ```

3. 发布内容
   ```bash
   python bilibili/master.py  # B站发布
   python zhihu/master.py  # 知乎发布
   ```

## 注意事项

- 请确保所有API密钥安全保存，不要提交到代码仓库
- 使用前请确认Fish Speech服务正常运行
- 视频处理可能需要较大的系统资源，请确保系统配置满足要求
- 建议定期备份生成的内容和配置文件

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。在提交代码前，请确保：
1. 代码符合项目的编码规范
2. 添加了必要的注释和文档
3. 所有测试用例通过

## 许可证

本项目采用 MIT 许可证
