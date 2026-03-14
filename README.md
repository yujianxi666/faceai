# faceai
一个通过Linux摄像头来远程给电脑开机的工具

闲得没事写了一个远程开机程序
对准摄像头比OK手势就行

安装依赖操作（要安装conda）：
sudo apt install -y cmake build-essential python3-dev libopenblas-dev wakeonlan libasound2-dev
conda create -n faceai python=3.10 -y
conda activate faceai
pip install mediapipe==0.10.14 opencv-python numpy pygame

在相同目录中放入以下文件
1.python主文件
2.你的人脸照片，格式如下
me1.jpg    （你的正面照）
me2.jpg    （左脸）
me3.jpg    （右脸）
me4.jpg    （抬头）
me5.jpg    （低头）

运行以下命令启动：
conda activate faceai
python trigger.py

参数设置：
THRESHOLD = 1.2 修改识别阈值
TARGET_MAC = "MAC地址"
MAX_FACE_SAMPLES = 5 最高人脸样本上限
