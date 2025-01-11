'''
Author: SheathedSharp z404878860@163.com
Date: 2024-06-06 12:57:12
'''
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

class ColorfulImageCompressor:
    def __init__(self, n_clusters, max_colors, resize_factor=0.5):
        """
        初始化彩色图像压缩器对象。

        参数：
        - n_clusters：聚类数，用于 KMeans 算法，指定图像中的颜色数量。
        - max_colors：最大颜色数，用于动态规划量化，指定压缩后图像中的最大颜色数量。
        - resize_factor：缩放因子，用于调整图像尺寸，默认为 0.5，表示将图像尺寸缩小到原始的一半。
        """
        self.n_clusters = n_clusters
        self.max_colors = max_colors
        self.resize_factor = resize_factor

    def compress(self, image_path, compressed_file_path):
        """
        压缩彩色图像并保存到指定路径。

        参数：
        - image_path：原始图像文件路径。
        - compressed_file_path：压缩后的图像文件路径。
        """
        # 打开图像并转换为 RGB 模式
        image = Image.open(image_path)
        image = image.convert('RGB')

        # 根据缩放因子调整图像大小
        new_size = (int(image.width * self.resize_factor), int(image.height * self.resize_factor))
        image = image.resize(new_size)

        # 将图像转换为 NumPy 数组并重塑为二维数组
        np_image = np.array(image)
        original_shape = np_image.shape
        np_image = np_image.reshape(-1, 3)

        # 使用动态规划量化对图像进行压缩
        compressed_data = self._dynamic_programming_quantization(np_image)

        # 保存压缩后的图像数据到指定路径
        np.savez_compressed(compressed_file_path, np_image=compressed_data['np_image'], original_shape=original_shape, n_clusters=self.n_clusters, max_colors=self.max_colors, center_colors=compressed_data['center_colors'])

    def decompress(self, compressed_file_path):
        """
        解压缩彩色图像并返回解压缩后的图像对象。

        参数：
        - compressed_file_path：压缩后的图像文件路径。

        返回：
        - reconstructed_image：解压缩后的图像对象。
        """
        # 加载压缩后的图像数据
        compressed_data = np.load(compressed_file_path)
        np_image = compressed_data['np_image'].reshape(-1, 3)
        center_colors = compressed_data['center_colors']

        # 根据聚类中心替换像素颜色
        for i in range(self.n_clusters):
            np_image[np_image[:, 0] == i] = center_colors[i]

        # 将重构后的图像数据重塑为原始形状
        original_shape = compressed_data['original_shape']
        reconstructed_image = np_image.reshape(*original_shape).astype('uint8')
        reconstructed_image = Image.fromarray(reconstructed_image, 'RGB')

        # 恢复图像原始尺寸
        original_size = (int(reconstructed_image.width / self.resize_factor), int(reconstructed_image.height / self.resize_factor))
        reconstructed_image = reconstructed_image.resize(original_size)

        return reconstructed_image

    def _dynamic_programming_quantization(self, image_array):
        """
        动态规划量化，将彩色图像颜色量化为指定数量的颜色。

        参数：
        - image_array：图像数据的 NumPy 数组表示。

        返回：
        - compressed_data：包含压缩后图像数据及相关信息的字典。
        """
        # 使用 KMeans 进行聚类
        kmeans = KMeans(n_clusters=self.n_clusters)
        labels = kmeans.fit_predict(image_array)
        quantized_image = np.zeros_like(image_array)

        # 遍历每个聚类簇
        for i in range(self.n_clusters):
            # 获取当前簇的像素颜色及其出现次数
            cluster_pixels = image_array[labels == i]
            unique_colors, color_counts = np.unique(cluster_pixels, axis=0, return_counts=True)
            
            # 选取出现次数最多的前 max_colors 个颜色作为量化后的颜色
            color_indices = np.argsort(color_counts)[::-1][:self.max_colors]
            quantized_colors = unique_colors[color_indices]

            # 计算聚类中像素与量化后颜色的距离
            distances = np.linalg.norm(cluster_pixels[:, None] - quantized_colors, axis=2)
            quantized_indices = np.argmin(distances, axis=1)

            # 使用量化后颜色替换聚类中的像素颜色
            quantized_image[labels == i] = quantized_colors[quantized_indices]

        # 存储聚类中心颜色
        center_colors = kmeans.cluster_centers_.astype('uint8')

        return {'np_image': quantized_image, 'n_clusters': self.n_clusters, 'max_colors': self.max_colors, 'center_colors': center_colors}


if __name__ == '__main__':
    # 使用方法
    image_path = "./img/image2.jpg"
    compressed_file_path = "./npz/compressed_image2_n4_c2.npz"

    compressor = ColorfulImageCompressor(n_clusters=4, max_colors=2, resize_factor=0.5)
    compressor.compress(image_path, compressed_file_path)

    reconstructed_image = compressor.decompress(compressed_file_path)
    reconstructed_image.show()
    reconstructed_image.save("./img/reconstructed_image2_n4_c2.jpg")
