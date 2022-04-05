## tensorflow 速度慢
![image-20220331201623509](note.assets/image-20220331201623509.png)

尝试以下解决方法
https://stackoverflow.com/questions/62681257/tf-keras-model-predict-is-slower-than-straight-numpy

关闭eager mode：

`tf.compat.v1.disable_eager_execution()`

![image-20220331201431802](note.assets/image-20220331201431802.png)

https://towardsdatascience.com/accelerate-your-training-and-inference-running-on-tensorflow-896aa963aa70

尝试model puring



## 网络不好收敛

## 网络过拟合

## 抽取数据缺乏代表性

抽样300次最优解步数

![image-20220405100953579](note.assets/image-20220405100953579.png)

![image-20220405103227758](note.assets/image-20220405103227758.png)

![image-20220405103238598](note.assets/image-20220405103238598.png)

