# faceai - 基于Linux摄像头的远程开机工具
一个通过Linux摄像头识别手势实现远程电脑开机的工具，对准摄像头比**OK手势**即可触发开机。

## 功能说明
通过摄像头实时检测人脸+OK手势，验证通过后发送网络唤醒指令，实现远程开机。

## 环境依赖安装
### 前置要求
已安装 **Conda** 环境

### 安装系统依赖
```bash
sudo apt install -y cmake build-essential python3-dev libopenblas-dev wakeonlan libasound2-dev
```

### 创建并激活Python虚拟环境
```bash
# 创建conda环境（Python 3.10）
conda create -n faceai python=3.10 -y

# 激活环境
conda activate faceai
```

### 安装Python依赖库
```bash
pip install mediapipe==0.10.14 opencv-python numpy pygame
```

## 所需文件
将以下文件放置在程序**同一目录**下：
1. 项目Python主程序文件
2. 人脸样本照片（共5张，严格按以下命名）：
   - `me1.jpg`：正面照
   - `me2.jpg`：左脸照
   - `me3.jpg`：右脸照
   - `me4.jpg`：抬头照
   - `me5.jpg`：低头照

## 运行方式
```bash
# 激活conda环境
conda activate faceai

# 启动程序
python trigger.py
```

## 核心参数配置
在代码中修改以下参数：
```python
# 人脸识别阈值（数值越小识别越严格）
THRESHOLD = 1.2

# 目标开机设备的MAC地址（必填）
TARGET_MAC = "你的设备MAC地址"

# 人脸样本最大数量（默认5张，无需修改）
MAX_FACE_SAMPLES = 5
```

## 使用说明
1. 启动程序后，摄像头自动开启
2. 正对摄像头，保持人脸在画面内
3. 比出**OK手势**，验证通过后自动发送开机指令
