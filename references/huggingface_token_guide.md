# HuggingFace Token 申请指南
# HuggingFace Token Application Guide

> 说话人分离功能需要 HuggingFace Token 才能使用
> Speaker diarization requires a HuggingFace Token

---

## 为什么需要 Token？ / Why Token is Required?

说话人分离使用 [pyannote.audio](https://github.com/pyannote/pyannote-audio) 模型，该模型托管在 HuggingFace 上，需要：
1. 接受模型使用协议
2. 使用 Token 进行身份验证

Speaker diarization uses pyannote.audio models hosted on HuggingFace, which requires:
1. Accepting model license agreement
2. Token authentication

---

## 申请步骤 / Application Steps

### 步骤 1: 注册 HuggingFace 账号 / Register Account

1. 访问 / Visit: https://huggingface.co/join
2. 填写邮箱、用户名、密码 / Fill in email, username, password
3. 或使用 GitHub/Google 账号登录 / Or use GitHub/Google login

### 步骤 2: 创建 Access Token / Create Token

1. 登录后访问 / After login, visit: https://huggingface.co/settings/tokens
2. 点击 **"New token"** 按钮 / Click **"New token"** button
3. 填写 Token 名称（随意，如 "pyannote"）/ Enter token name (any name, e.g., "pyannote")
4. **权限选择 "Read"** (只需要读取权限) / **Select "Read" permission**
5. 点击 **"Generate a token"** / Click **"Generate a token"**
6. **复制生成的 Token**（以 `hf_` 开头）/ **Copy the generated token** (starts with `hf_`)

⚠️ Token 只显示一次，请妥善保存！
⚠️ Token is shown only once, save it securely!

### 步骤 3: 接受模型使用协议 / Accept License

访问以下链接并点击 **"Agree and access repository"**:
Visit the following links and click **"Agree and access repository"**:

1. https://huggingface.co/pyannote/speaker-diarization-3.1
2. https://huggingface.co/pyannote/segmentation-3.0

必须接受协议才能下载模型！
You must accept the license to download models!

### 步骤 4: 设置环境变量 / Set Environment Variable

**Windows (CMD):**
```cmd
setx HUGGINGFACE_TOKEN "hf_your_token_here"
```

**Windows (PowerShell):**
```powershell
[Environment]::SetEnvironmentVariable("HUGGINGFACE_TOKEN", "hf_your_token_here", "User")
```

**Linux/Mac:**
```bash
echo 'export HUGGINGFACE_TOKEN="hf_your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

或者告诉 AI / Or tell AI:
> 中文: "请帮我设置 HuggingFace Token: hf_your_token_here"
> English: "Please set my HuggingFace Token: hf_your_token_here"

---

## 验证 Token / Verify Token

告诉 AI / Tell AI:
> 中文: "请验证我的 HuggingFace Token 是否有效"
> English: "Please verify my HuggingFace Token is valid"

或运行 / Or run:
```bash
python -c "import os; print('Token:', os.environ.get('HUGGINGFACE_TOKEN', 'Not set')[:10] + '...')"
```

---

## 常见问题 / FAQ

### Q: Token 忘记保存了怎么办？ / Forgot to save token?
A: 在 https://huggingface.co/settings/tokens 删除旧 Token，重新创建新的。
A: Delete old token at https://huggingface.co/settings/tokens and create a new one.

### Q: 提示 "Repository not found" 错误？ / "Repository not found" error?
A: 请确认已接受步骤3中两个模型的使用协议。
A: Make sure you accepted both model licenses in Step 3.

### Q: 可以不用 Token 吗？ / Can I skip the token?
A: 说话人分离必须使用 Token。如果不需要此功能，可以跳过。
A: Token is required for speaker diarization. Skip if you don't need this feature.

---

## 隐私说明 / Privacy Note

- Token 只存储在您本地电脑 / Token is stored locally only
- 模型下载后也保存在本地 (~/.cache/huggingface) / Models are cached locally
- 所有转录处理都在本地完成 / All processing happens locally
- 不会上传任何音视频数据到云端 / No audio/video data uploaded to cloud

Your data stays on your machine. 100% private.
