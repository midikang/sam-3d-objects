# Windows 10 运行 Web 界面指南

本指南专门针对在 Windows 10 上运行 SAM 3D Objects Web 应用。

## 快速开始

### 前置条件

1. **硬件要求**
   - NVIDIA GPU（至少 32 GB 显存）
   - Windows 10 64位操作系统

2. **软件要求**
   - [Anaconda](https://www.anaconda.com/download) 或 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
   - [CUDA Toolkit 12.1](https://developer.nvidia.com/cuda-downloads)
   - [Git for Windows](https://git-scm.com/download/win)

### 安装步骤

#### 1. 安装 CUDA

从 [NVIDIA 官网](https://developer.nvidia.com/cuda-downloads) 下载并安装 CUDA Toolkit 12.1。

安装后验证：
```cmd
nvcc --version
```

#### 2. 创建 Python 环境

打开 Anaconda Prompt 或命令提示符：

```cmd
# 创建新的 conda 环境（Python 3.11）
conda create -n sam3d-objects python=3.11 -y
conda activate sam3d-objects
```

#### 3. 安装 PyTorch（支持 CUDA）

```cmd
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121
```

#### 4. 安装项目依赖

```cmd
# 设置环境变量
set PIP_EXTRA_INDEX_URL=https://pypi.ngc.nvidia.com https://download.pytorch.org/whl/cu121

# 安装 sam3d-objects
pip install -e .

# 安装 PyTorch3D（可能需要一些时间）
conda install -c conda-forge pytorch3d -y

# 安装推理依赖
set PIP_FIND_LINKS=https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.5.1_cu121.html
pip install -e .[inference]
```

#### 5. 应用 Hydra 补丁

```cmd
python patching\hydra
```

#### 6. 下载模型检查点

首先，在 [Hugging Face](https://huggingface.co/facebook/sam-3d-objects) 上请求访问权限。

获得批准后，登录：

```cmd
pip install "huggingface-hub[cli]<1.0"
huggingface-cli login
```

然后下载检查点：

```cmd
set TAG=hf
huggingface-cli download --repo-type model --local-dir checkpoints\%TAG%-download --max-workers 1 facebook/sam-3d-objects
move checkpoints\%TAG%-download\checkpoints checkpoints\%TAG%
rmdir /s /q checkpoints\%TAG%-download
```

## 运行 Web 界面

安装完成后，有三种方式启动 Web 界面：

### 方式一：使用批处理文件（最简单）

直接双击 `launch_web_demo.bat` 文件，或在命令提示符中运行：

```cmd
launch_web_demo.bat
```

### 方式二：使用 PowerShell 脚本

右键点击 `launch_web_demo.ps1` 并选择"使用 PowerShell 运行"，或在 PowerShell 中：

```powershell
.\launch_web_demo.ps1
```

### 方式三：手动启动

```cmd
# 激活环境
conda activate sam3d-objects

# 运行 Web 演示
python web_demo.py
```

## 访问 Web 界面

启动后，在浏览器中打开：

```
http://localhost:7860
```

## 使用说明

1. **上传图片**：在左侧上传一张 RGB 图片
2. **上传遮罩**：上传对应的遮罩图片（白色区域表示要重建的物体）
3. **设置随机种子**（可选）：用于可重复的结果
4. **点击"Generate 3D Model"**：开始生成 3D 模型
5. **查看结果**：在右侧查看生成的 3D 高斯泼溅模型

## 高级选项

可以使用命令行参数自定义设置：

```cmd
# 更改端口
python web_demo.py --port 8080

# 创建公共分享链接
python web_demo.py --share

# 禁用模型编译（启动更快，但推理较慢）
python web_demo.py --no-compile

# 允许外部连接
python web_demo.py --server-name 0.0.0.0
```

## 常见问题

### 问题：PyTorch3D 安装失败

**解决方案**：
```cmd
conda install -c conda-forge pytorch3d -y
```

如果还是失败，可以从源代码编译：
https://github.com/facebookresearch/pytorch3d/blob/main/INSTALL.md

### 问题：CUDA 内存不足

**解决方案**：
- 确保 GPU 至少有 32 GB 显存
- 关闭其他使用 GPU 的程序
- 使用 `nvidia-smi` 检查 GPU 内存使用情况

### 问题：找不到 CUDA

**解决方案**：
- 确保已安装 CUDA Toolkit
- 将 CUDA 的 bin 目录添加到系统 PATH 中
- 重启命令提示符或 Anaconda Prompt

### 问题：kaolin 或 gsplat 安装失败

**解决方案**：
这些包可能需要在 Windows 上编译。请参考各自的 GitHub 仓库获取 Windows 安装说明。

### 问题：Visual Studio 构建工具错误

**解决方案**：
一些 Python 包需要 C++ 编译器。下载并安装：
https://visualstudio.microsoft.com/downloads/ (选择"Build Tools for Visual Studio")

## 性能说明

- 首次运行会较慢（模型编译）
- 后续运行会更快
- 推理时间取决于您的 GPU 性能

## 获取帮助

如果遇到问题，请查看：
- 详细的 Windows 设置指南：`doc/setup_windows.md`
- Linux 设置指南：`doc/setup.md`
- 主 README：`README.md`

## 不使用 Web 界面

如果 Web 界面有问题，也可以使用命令行演示：

```cmd
python demo.py
```

这将处理示例图像并保存结果到 `splat.ply`。

---

**注意**：此项目需要强大的 GPU。确保您的系统满足最低要求（32 GB VRAM）。
