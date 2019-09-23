# license-plate-recognition

By 郑煜伟

基于tensorflow和keras，利用多标签分类模型，实现车牌识别。

## 场景说明 及 困难/挑战
车牌识别大致场景有：
1. 闸门场景；
1. 车位场景；
1. 交通道路场景；

本算法大致流程为：通过目标检测/关键点检测等方式，获取车牌部分作为本算法（多标签多分类模型）输入，最终预测出车牌号。

本算法主要解决车位场景（闸门场景比车位场景简单些，因为车一般正对且有摄像头灯光矫正），存在以下挑战：  
1. 异常数据：标签不正确，车牌截断；  
1. 数据差异大：上一步检测得到的车牌存在波动，室外停车点环境变化（复杂的光影效果，雾霾效果），车牌角度变化大；  
1. 类间数据不平衡：个别省份特别少，特殊车牌特别少，个别省份特别多；  
1. 车牌数据分批收集、车牌类型、业务场景多样化：澳门车牌、双行车牌等（具有较强的模型能力，同时要防止数据量少时过拟合），
多平台部署（端/云侧模型）；  
1. 商用指标严格：指定置信度下，准确率99.9%，召回率80%以上；闸门的总体准确率99.9%以上。   

拟解决的算法设计方案：
1. 标签不正确：可通过模型迭代，逐渐修正解决；
2. 样本难度差异大，不可识别，异常数据：GHM，降低简单样本、异常样本的梯度影响；
3. 难以识别，复杂的光影效果，车牌数据分批收集：数据增强（增强对环境影响的鲁棒性、数据量问题），数据预处理（白化，降低环境波动），
RAdam：warmup（1. 减缓模型在初始阶段对样本复杂信息的过拟合现象（平稳探索参数空间）；
2. 因为样本差异大且前期梯度大，小学习率可以保持模型深层的稳定性；3. 自适应学习，快速迭代降低学习率调参时间及难度）；
4. 类间数据不平衡：类间数据balance（正交梯度，few-shot）；
5. 较强的模型能力，较快的推理速度：剪枝（slim），模型蒸馏；（nas？）

## 目录结构

- `A_learning_notes`: README后，**先查看本部分**了解本项目大致结构；
- `backbone`: 模型的骨干网络脚本；
- `dataset`: 数据集构造脚本；
    - `dataset_util.py`: 使用tf.image API进行图像数据增强，然后用tf.data进行数据集构建；
    - `file_util.py`: 以txt标签文件的形式，构造tf.data数据集用于训练；
    - `tfrecord_util.py`: 读取txt标签文件，写tfrecord，然后读取tfrecord为数据集用于训练；
- `images`: 项目图片；
- `logs`: 存放训练过程中的日志文件和tensorboard文件（当前可能不存在）；
- `models`: 存放训练好的模型文件（当前可能不存在）；
- `multi_label`: 多标签分类模型构建脚本；
    - `classifier_loss.py`: 多标签分类的损失函数，包含多种损失函数：`focal loss`、`GHM`等；
    - `classifier_model.py`: 多标签分类模型，负责调用`backbone`里的骨干网络和本脚本中的多标签`head`组成整体模型；
    - `train.py`: 模型训练接口，集成模型构建/编译/训练/debug/预测、数据集构建等功能；
- `utils`: 一些工具脚本；
    - `generate_txt`: 扫描指定路径下的图片数据，生成训练、测试等label.txt；
    - `logger_callback.py`: 日志打印的keras回调函数；
- `configs.py`: 配置文件；
- `run.py`: 启动脚本；


## 算法说明

在**多标签多分类模型**基础上，添加功能：
- loss函数改造：
    - `label smoothing`: 标签平滑。
    - `focal loss`: 给每个样本的分类loss增加一个因子项，降低分类误差小的样本的影响，解决难易样本问题。
    > ![focal loss类别概率和损失关系图](https://github.com/zheng-yuwei/multi-label-classification/tree/master/images/focal-loss.jpg)
    - `gradient harmonizing mechanism (GHM)`: 
    根据样本梯度密度曲线（这里的梯度是梯度范数，并且不是所有网络参数的梯度，而是最后一层的回传梯度），
    取反得到梯度密度调和参数（和平衡多类别数据集一个意思，只不过这里不是按类别来平衡，而是按梯度区间来平衡），
    再乘以梯度以**调整梯度贡献曲线**，从而降低高密度区域的梯度贡献比例，提升低密度区域的梯度贡献比例。
    > ![GHM论文梯度分布与贡献图](https://github.com/zheng-yuwei/multi-label-classification/tree/master/images/GHM-insight.jpg)
    >
    > 原论文insight： 对网络训练而言，梯度是最重要的东西，而网络训练不好，也是因为梯度没调节好。
    focal loss认为前背景不平衡问题，本质为难易样本不平衡问题，从而调节样本的梯度贡献，一定程度上解决了背景问题。
    作者认为，类别不平衡、难易样本不平衡，造成的本质驱动是梯度不平衡。
    > 然后通过绘制训练好的模型在样本空间上的梯度分布曲线，发现小梯度和大梯度都是高密度区域，
    （作者认为小梯度对应易学习样本，大密度对应异常样本）；
    然后绘制正常loss和focal loss梯度贡献曲线，发现正常loss中，高密度区域的梯度贡献度很高，
    而focal loss中，小梯度的高密度区域被因子项惩罚而降低梯度贡献度，
    但大梯度的高密度区域的梯度贡献度依然很高。
    作者认为focal loss平衡了一部分梯度贡献度，所以使得训练低密度的中间梯度的梯度贡献度影响提升，
    提升了算法性能；同时，认为focal loss并没有从本质出发，所以还有残留问题（异常样本大梯度的高密度区域）。
    然后提出了GHM，从梯度分布和梯度贡献角度出发，提升网络训练效果。
    
- 分离conv层的权重衰减项$\lambda_{conv}$ 和 BN层gamma的权重衰减项$\lambda_{gamma}$  


## Tips & Conclusion:

对最终训练结果的影响依次降低（这个可以忽略，因为我用超级小的数据集跑着完下而已）。

- 网络结构：这个决定一切。我就把其中一层进行了修改：激活函数为relu、激活函数为linear、去掉该层、修改该层宽度。
其中激活函数为relu的完爆其他，而在relu的基础上，修改宽度也会有一定影响；
（或者某种意义上，这个现象说明了深度决定一切）
但是，我实际训练过程中，模型过拟合了！！！

- batch size：大肯定是越好的，然后发现 (batch-size % total-size) != 0 也能提升效果，可能是shuffle得更好；
（这个好像效果比增加宽度好，可能是我数据量小（用了12张图片做实验，因为**用少量数据验证代码**，所以希望过拟合），
模型拟合能力已经够了，但是不好好shuffle会形成震荡效果（我用的adam），最终模型会收敛不好）

- warm up: 这个是**墙裂推荐**
> 通过设置相同的随机数 `np.random.seed(x)`, `tf.set_random_seed(y)`，保证模型初始化状态一致
> 其他超参设置一致的情况下，设置训练的learning rate：
> - step_epoch = [40, 80, 120, 160, 200], step_lr = [0.0002, 0.00002, 0.000002, 0.000002, 0.000002, ]
> - step_epoch = [40, 80, 120, 160, 200], step_lr = [0.000002, 0.0002, 0.00002, 0.000002, 0.000002, ]    
>
> 结果上warm up的效果完爆没warm up的。
> 
> 同时，我也比较了warm up的epoch的影响。原始warm up论文中建议5个epoch。
> 我的实验结果是太大和太小都不太好（虽然比没有warm up都有所提升，同时宜大不宜小）。
> 如果是用adam等自适应算法，前期收敛快，后期loss不低，训练/测试效果都不好，可以加warm up试试；

- 权重初始化：祈求上帝抛个好骰子；

- 权重衰减：基本建议就是，ref 论文中的L2权重衰减的量级。

## 缓解过拟合/标注错误/样本错误（效果不分先后，根据实现难度来）
1. 一定程度提高BN层中gamma的L2权重衰减，conv层的L2权重衰减可以维持不变；[1,2,3]
1. 加大batch，然后要用warmup（我一开始用adam+warmup,后面用radam+warmup, radam中用动态学习率）；[4,5,6]
1. 白化预处理；
1. label smoothing:；[7]
1. 数据增强（增加数据量）；
1. 修改网络结构，resnext18相比resnet18多了结构正则的作用，效果好些；
1. GHM损失函数；[8]
1. 剪枝，其实和修改网络结构一个道理，只不过剪枝可以类似NAS自动找到更好的sub-network(网络结构)；[3,9,10]

TIPS：其他试过但基本无效的手段包括：
继续加大weight decay权重，BN层的gamma不加weight decay，BN层的beta加weight decay，
全连接层加dropout，focal loss，从Adam训练改为SGDM，加warmup。

(该表已过期，最终最有方案是：  
**[0.00001, 0.001, 0.0001, 0.00001, 0.000001]的warmup RAdam + conv 5e-4的weight decay + BN lambda 1e-3的slim + whiting + 
augment + [30bins, 0.75LWMA] label-wise的ghm + 
resnet18(最后一个block为384而非512，这个并没有实验过，随手设置小一点而已；
conv层没有bias，影响会被BN层消除，并且实验后的确也比较好）**  
实际测试集上，总准确率98+%，指定置信度召回率85+%，准确率99.9+%；在闸门这种简单场景下可达到99.9+%)

|   model  | weight-decay | whiting | augment | label smoothing |   backbone   | GHM-loss | prune | acc   | recall |  
| :------: | :----------: | :-----: | :-----: | :-------------: | :----------: | :------: | :---: | :---: | :----: | 
| baseline |     1e-6     |    x    |    x    |        x        |   resnet19   |     x    |   x   | 0.76  |  0.40  |
|    v1    |     5e-4     |    x    |    x    |        x        |   resnet19   |     x    |   x   | 0.86  |  0.58  |
|    v2    |     5e-4     |    √   |    x    |        x        |   resnet19   |     x    |   x   | 0.87  |  0.67  |
|    v3    |     5e-4     |    √   |    √   |        x        |   resnet19   |     x    |   x   | 0.95  |  0.76  |
|    v4.0  |     5e-4     |    √   |    √   |        x        |   resnet18   |     x    |   x   | 0.9949|  0.802 |
| v4-RAdam |     5e-4     |    √   |    √   |        x        |   resnet18   |     x    |   x   | 0.9960|  0.8576|
|    v4.1  |     5e-4     |    √   |    √   |        x        |  resnet18-v2 |     x    |   x   | 0.961 |  0.757 |
|    v4.2  |     5e-4     |    √   |    √   |        x        |   resnext18  |     x    |   x   | 0.9971|  0.753 |
|    v4.3  |     5e-4     |    √   |    √   |        x        |   mobilenet  |     x    |   x   |   -   |    -   |
|    v4.4  |     5e-4     |    √   |    √   |        x        | mobilenet-v2 |     x    |   x   |   -   |    -   |
|    v4.5  |     5e-4     |    √   |    √   |        x        | mobilenet-v3 |     x    |   x   |   -   |    -   |
|    v5    |     5e-4     |    √   |    √   |        √       |   resnet18   |     x    |   x   | 0.9968|  0.82  |
|    v6    |     5e-4     |    √   |    √   |        x        |   resnet18   |     √   |   x   | 0.9979|  0.816 |
|    v6    |     5e-4     |    √   |    √   |        x        |   resnet18   |   multi  |   x   | 0.9986|  0.823 |
|    v7    |     5e-4     |    √   |    √   |        x        |   resnet18   |     x    |   √  |   -   |    -   |

** 其中，acc和recall指测试集的基于0.95置信度以上的准确度和召回率。训练集上这两个指标基本都可以达到0.99以上；
后续v4.0及之后，置信度改为0.85；
** GHM-loss中，multi表示每个label使用各自的gradient做density harmonized mechanism，否则综合所有label的gradient做GHM；
** 都用Adam训练，除了指定用RAdam。

[1] L2 Regularization versus Batch and Weight Normalization  
[2] Towards Understanding Regularization in Batch Normalization  
[3] Learning Efficient Convolutional Networks through Network Slimming  
[4] Accurate, Large Minibatch SGD：Training ImageNet in 1 Hour  
[5] Large Batch Training of Convolutional Networks  
[6] On the Variance of the Adaptive Learning Rate and Beyond  
[7] Rethinking the inception architecture for computer vision  
[8] Gradient Harmonized Single-stage Detector  
[9] Data-Driven Sparse Structure Selection for Deep Neural Networks  
[10] Rethinking the Value of Network Pruning

## TODO
1. self-balance
1. Handwriting Recognition in Low-resource Scripts Using Adversarial Learning
1. 检测模型和识别模型之间的gap：双模型的好处在于训练隔离，从而可以独立设置策略/技巧（预处理、数据增强、算法设置）、数据集处理（外源车牌图像、矫正）等；
坏处在于需要人工介入，进行接合，同时没有end-to-end的信息交流共享；

