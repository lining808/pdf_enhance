# pdf_enhance
对扫描的pdf（不适用于文字版）文件进行质量提升，字体清晰去除杂色，优化大小。优化效果如下图
![Uploading 微信截图_20231213155947.png…]()
![Uploading 微信截图_20231213160059.png…]()


# 使用方法
调用以下函数。

one_hot(r'E:\Code\Python\csdn\image\强化学习（第2版）.pdf', 1.3, 1.5, 1.3, 1.0, zoom=4)

其中参数解释为：

pdf_path, pdf文件地址

bright=1.0, 亮度增强，0为最暗，10为最亮，1为pdf当前亮度

contrast=1.0, 对比度增强，0为最低，10为最高，1为pdf当前对比度

color=1.0, 色彩增强，0为最淡，10为最深，1为pdf当前色彩

sharpness=1.0, 锐化增强，0为最小，10为最大，1为pdf当前

saveFolderPath=None, 保存地址，不填则为当前目录

zoom=1，pdf缩放大小
