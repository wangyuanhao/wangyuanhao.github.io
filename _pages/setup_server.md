# 将已有深度学习环境打包到离线服务器上的方法

注意：打包环境与目标服务器应尽量是同一平台，例如 Linux x86_64 到 Linux x86_64；不要从 Mac/Win 直接打包给 Linux 服务器用。我自己的操作系统及版本是Ubuntu 22.04 / Linux x86_64， 显卡是4090.

### Step 1: 在联网的Linux上打包已有环境

```
# 获取当前环境列表
conda env list

# 假设已有环境叫myconda, 在base环境中对其进行打包
conda activate base
pip install conda-pack

# 将myconda打包为tar.gz文件
conda pack -n myconda -o myconda_env.tar.gz

# 或按路径打包
conda pack -p /home/user/miniconda3/envs/myconda -o myconda_env.tar.gz
```

* 这里提供我自己用的已经打包好的conda环境，如果需要使用可以直接跳过Step 1。下载地址 https://pan.baidu.com/s/1bq479HDpb0KDvsJmpAJ7mA ，提取码: jgxh 。里面的python packages包括：

```
Package                  Version

------------------------ ------------

absl-py                  2.4.0
aiohappyeyeballs         2.6.2
aiohttp                  3.14.1
aiosignal                1.4.0
attrs                    26.1.0
certifi                  2026.6.17
charset-normalizer       3.4.7
filelock                 3.13.1
frozenlist               1.8.0
fsspec                   2024.6.1
grpcio                   1.81.1
idna                     3.18
Jinja2                   3.1.4
joblib                   1.5.3
Markdown                 3.10.2
MarkupSafe               2.1.5
mpmath                   1.3.0
multidict                6.7.1
narwhals                 2.23.0
networkx                 3.3
numpy                    2.1.2
nvidia-cublas-cu12       12.4.5.8
nvidia-cuda-cupti-cu12   12.4.127
nvidia-cuda-nvrtc-cu12   12.4.127
nvidia-cuda-runtime-cu12 12.4.127
nvidia-cudnn-cu12        9.1.0.70
nvidia-cufft-cu12        11.2.1.3
nvidia-curand-cu12       10.3.5.147
nvidia-cusolver-cu12     11.6.1.9
nvidia-cusparse-cu12     12.3.1.170
nvidia-cusparselt-cu12   0.6.2
nvidia-nccl-cu12         2.21.5
nvidia-nvjitlink-cu12    12.4.127
nvidia-nvtx-cu12         12.4.127
packaging                26.2
pandas                   3.0.3
pillow                   11.0.0
pip                      25.1
propcache                0.5.2
protobuf                 7.35.1
psutil                   7.2.2
pyparsing                3.3.2
python-dateutil          2.9.0.post0
requests                 2.34.2
scikit-learn             1.9.0
scipy                    1.17.1
setuptools               78.1.1
six                      1.17.0
sympy                    1.13.1
tensorboard              2.21.0
tensorboard-data-server  0.7.2
threadpoolctl            3.6.0
torch                    2.6.0+cu124
torch-geometric          2.8.0
torchaudio               2.6.0+cu124
torchvision              0.21.0+cu124
tqdm                     4.68.3
triton                   3.2.0
typing_extensions        4.12.2
urllib3                  2.7.0
Werkzeug                 3.1.8
wheel                    0.45.1
xxhash                   3.8.0
yarl                     1.24.2
```

### Step 2: 将已经打包好的环境tar.gz压缩文件上传到离线服务器

```
# Windows环境可以使用WinSCP软件，或者使用scp、rsync命令行，此处提供rsync的用法
rsync -av --progress -e "ssh -p 端口号" your_local_path/myconda_env.tar.gz username@server_ip:/server/target/path/

## 要按需修改的字段 ##
# 端口号：ssh连接的端口号
# your_local_path: myconda_env.tar.gz在本地的目录位置
# username:离线服务器的用户名
# server_ip：离线服务器IP
# /server/target/path/: 上传到离线服务器的路径，需要首先创建
```

* 直接使用WinSCP可以省去很多麻烦，端口号、用户名及服务器IP可以在"衍生智算系统—>容器环境——>SSH登录"处看到。

### Step 3: 在离线服务器上配置conda环境

```
# 登录离线服务器后，在离线服务器上解压, 创建解压路径(可自行定义路径位置)
mkdir -p /root/envs/myconda

# 将tar.gz文件解压到/root/envs/myconda
tar -xzf /server/target/path/myconda_env.tar.gz -C /root/envs/myconda

# 先把解压出来的 conda 环境加入 PATH，如果正常，which python 应该返回：/root/envs/myconda/bin/python
export PATH=/root/envs/myconda/bin:$PATH
which python


# 修复环境路径，只需执行一次
/root/envs/myconda/bin/conda-unpack

# 激活环境，注意每次使用环境之前需要执行下面的source命令
source /root/envs/myconda/bin/activate

# 测试CUDA可用性
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.version.cuda)"

# 离开环境
source /root/envs/myconda/bin/deactivate
```

### 其他说明

* 其他package可以先下载wheel上传到离线服务器再激活conda环境后用pip安装；
* 其他配置方法包括直接下载好Anaconda/Miniconda和需要的package的wheel文件上传到离线服务器上安装；
* 我的离线服务器版本是4090，也就是myconda_env.tar.gz的安装只是在4090的配置下成功，其他显卡未知；
* 这些安装方法在每次配置环境的时候都很耗时间，而且计算资源归还后再申请使用需要重新安装一次，建议：
  * 如果可行，现在的服务器应该具备访问外网的功能；
  * 现在的算力平台应该具备可选的配置基本深度学习、R语言等开发环境的系统镜像，实现创建容器资源时开发环境的一键配置，目前这些功能都是算力租用平台的基本功能了。