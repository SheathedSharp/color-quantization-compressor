<!--
 * @Author: SheathedSharp z404878860@163.com
 * @Date: 2025-01-11 15:23:58
-->
<div align="center">
  
  [![Static Badge](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-%40SheathedSharp-red)](https://github.com/SheathedSharp/color-quantization-compressor/blob/main/README_CN.md)    |  [![Static Badge](https://img.shields.io/badge/English-%40SheathedSharp-blue)](https://github.com/SheathedSharp/color-quantization-compressor/blob/main/README.md)) 
  
</div>

# color-quantization-compressor
这是基于KMeans聚类和动态规划的彩色图像压缩工具。

## 主要功能以及结构
- 图像压缩：
    - 支持调整图像尺寸
    - 使用 KMeans 进行颜色聚类
    - 通过动态规划进行颜色量化

- 文件结构：
    - 图像文件存储（img 目录）
    - 压缩数据存储（npz 目录）
    - 核心压缩类（colorful_image_compressor.py）
    - 使用示例（example.py）

- 主要参数：
    - n_clusters：颜色聚类数
    - max_colors：最大颜色数
    - resize_factor：图像缩放因子

## 测试
测试图片我们使用的采用的一张818*818分辨率，大小为79.49KB的彩色图片。分别使用不同的聚类数量和颜色数量来进行测试。
| ![description](./demo/demo1.png) | ![description](./demo/demo2.png) |
|:---:|:---:|
| 原始图片	 | 聚类数为8，颜色为2的压缩图片 |


详细运行数据如下表（下面文件名中的n为聚类数，而c为颜色数）：
| 文件名                       | 原始大小（KB） | 压缩后的中间文件大小（KB） | 解压缩后的图片大小 (KB) | 
|------------------------------|---------------|--------------------------|-----------------------|
| reconstructed_image2_n4_c2   | 79.49         | 29.5                     | 41.7                  |          |
| reconstructed_image2_n4_c4   | 79.49         | 49.3                     | 45.2                  |          |
| reconstructed_image2_n4_c8   | 79.49         | 70.9                     | 51.3                  |          |
| reconstructed_image2_n4_c16  | 79.49         | 94.3                     | 59.3                  |          |
| reconstructed_image2_n8_c2   | 79.49         | 48.3                     | 48.7                  |          |
| reconstructed_image2_n8_c4   | 79.49         | 73.3                     | 52.5                  |          |
| reconstructed_image2_n8_c8   | 79.49         | 101                      | 59.1                  |          |
| reconstructed_image2_n8_c16  | 79.49         | 125                      | 61.1                  |          |