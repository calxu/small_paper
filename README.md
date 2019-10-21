# 硕士小论文

论文题目：Inferring Social Ties from Multi-view Spatiotemporal Co-occurrence


## 环境说明

1. python3 环境

2. 实验中 word2vec 是自行编译的，实验可以用gensim包取代

3. 实验中 LDA 是自行编译的，实验可以用gensim包取代


## 数据说明

使用的开源数据，可到[数据源下载](https://snap.stanford.edu/data/)Brightkite和Gowalla数据集；


## 目录结构

下面对实验目录结构作以下说明

* ./asset ：小论文原文，可Google检索；

* ./src ：源码文件；
    
    * ./src/1_imbalance_data ：处理数据不平衡问题，并生成训练和测试集样本；

    * ./src/2_baseline_features ：生成基准特征源码文件；

    * ./src/2_topic_features ：生成主题特征源码文件；

    * ./src/2_context_cooccurrence ：生成上下文特征源码文件；

    * ./src/3_* 文件说明：
      
        * ./src/3_baseline_predict_individually.py ：基准特征独立进行预测；

        * ./src/3_baseline_predict_merge.py ：基准特征融合进行预测；

        * ./src/3_topic_cooccurrence_predict.py ：主题特征进行预测；

        * ./src/3_context_cooccurrence_predict.py ：上下文特征进行预测；

        * ./src/4_feature_merge.py ：特征融合进行预测；

* ./result ： 效果文件，可视化PR曲线；


## 参考文献

1. Inferring Social Ties from Multi-view Spatiotemporal Co-occurrence
