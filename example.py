'''
Author: hiddenSharp429 z404878860@163.com
Date: 2024-06-06 12:57:12
LastEditors: hiddenSharp429 z404878860@163.com
LastEditTime: 2024-07-03 17:13:25
FilePath: /colorful_Image_compressor/example.py
Description: 
'''
from colorful_Image_compressor import ColorfulImageCompressor

if __name__ == '__main__':
    # 定义图像文件路径和压缩文件路径
    image_path = "./img/image2.jpg"
    compressed_file_path = "./npz/compressed_image2_n4_c2.npz"

    # 创建压缩器对象
    compressor = ColorfulImageCompressor(n_clusters=4, max_colors=2, resize_factor=0.5)

    # 压缩图像
    compressor.compress(image_path, compressed_file_path)

    # 解压缩图像
    reconstructed_image = compressor.decompress(compressed_file_path)

    # 显示图像
    reconstructed_image.show()

    # 保存图像
    reconstructed_image.save("./img/reconstructed_image2_n4_c2.jpg")
