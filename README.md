# CEA-Downloader

> 计算机工程与应用(CEA)  期刊自动下载工具

## 简介

[计算机工程与应用](http://cea.ceaj.org/CN/column/column105.shtml) 官方提供了该期刊的每篇文章下载链接，但是没有提供整期合并后的文档。为了方便阅读，该工具实现了期刊的自动下载，合并，添加书签功能。

## 使用说明

### 1. 安装环境

1. 安装 python3 后，使用命令安装依赖库。

```
pip install -r requirements.txt
```

### 2. 获取需要下载的文档编号

以2020年56卷20期为例：

1、 打开期刊 [官网](http://cea.ceaj.org/CN/volumn/home.shtml) 找到需要下载那期。

![image-20201024165239285](https://i.loli.net/2020/10/24/9C8NlI1pWbjAEiV.png)

2、查看起始，终止编号：

查看次目0的链接如下

```
2020年第20期
http://cea.ceaj.org/CN/abstract/abstract39078.shtml
```

其中编号：39078 为起始编号。

查看最后一篇论文的下载链接：

```
跨层穿梭车双提升机系统料箱拣选任务调度
http://cea.ceaj.org/CN/abstract/abstract39117.shtml
```

其中编号:  39117为终止编号。

3、 开始下载

```
python cea-dl.py -s 39078 -e 39117 -o .\save
参数说明： 
	-s start 起始编号
	-e end 终止编号
	-o output path 保存路径
```

执行完毕后会将所有文章下载到 `-o` 参数指定的路径下，若路径不存在则自动创建。

## 3. 结果演示

输出路径下

`{数字}.pdf` ：为每篇论文根据编号保存。

`merge_all.pdf`: 为所有论文合并后的版本。

`merge_all-bookmarked.pdf`: 为添加书签后的版本.

 	注：由于书签生成使用PDF解析后使用正则匹配，当前测试输出的书签均正常。不保证未来由于文档格式的变化导致书签添加一定正确。

![image-20201024170206003](https://i.loli.net/2020/10/24/gGacOxWLu8jXhtp.png)

![image-20201024170222589](https://i.loli.net/2020/10/24/2oksmzlNpwv6i9D.png)