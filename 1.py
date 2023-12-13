from PIL import Image, ImageEnhance
import os
import fitz


def image_enhance(imageFilePath, bright=1.0, contrast=1.0, color=1.0, sharpness=1.0, saveFolderPath=None):
    """
    图像增强之亮度、对比度与饱和度调整
    :param imageFilePath: 图像文件路径
    :param bright: 亮度
    :param contrast: 对比度
    :param color: 饱和度
    :param sharpness: 清晰度
    :param saveFolderPath: 结果保存路径
    :return:
    """

    imageFileName = os.path.basename(imageFilePath)
    imageOriginal = Image.open(imageFilePath)
    # 亮度调整
    brightEnhancer = ImageEnhance.Brightness(imageOriginal)
    imageBright = brightEnhancer.enhance(bright)

    # 对比度调整
    contrastEnhancer = ImageEnhance.Contrast(imageBright)
    imageContrast = contrastEnhancer.enhance(contrast)

    # 饱和度调整
    colorEnhancer = ImageEnhance.Color(imageContrast)
    imageColor = colorEnhancer.enhance(color)

    # 清晰度调整
    SharpnessEnhancer = ImageEnhance.Sharpness(imageColor)
    imageSharpness = SharpnessEnhancer.enhance(sharpness)

    if saveFolderPath is None:
        saveFolderPath = os.path.dirname(imageFilePath) + '/enhance'
        os.makedirs(saveFolderPath, exist_ok=True)
    imageBrightFilePath = os.path.join(saveFolderPath, imageFileName)
    imageSharpness.save(imageBrightFilePath)
    return


def combine_imgs_pdf(folder_path, pdf_file_path):
    """
    合成文件夹下的所有图片为pdf
    Args:
        folder_path (str): 源文件夹
        pdf_file_path (str): 输出路径
    """
    files = os.listdir(folder_path)
    png_files = []
    sources = []
    for file in files:
        if 'png' in file or 'jpg' in file:
            png_files.append(folder_path + file)
    png_files.sort()

    output = Image.open(png_files[0])
    png_files.pop(0)
    for file in png_files:
        png_file = Image.open(file)
        if png_file.mode == "RGB":
            png_file = png_file.convert("RGB")
        sources.append(png_file)
    output.save(pdf_file_path, "pdf", save_all=True, append_images=sources)


def pdf_image(pdfPath, zoom_x=1, zoom_y=1, rotation_angle=0, imgPath=None):
    """
    :param pdfPath: pdf文件的路径
    :param imgPath: 图像要保存的文件夹
    :param zoom_x: x方向的缩放系数
    :param zoom_y: y方向的缩放系数
    :param rotation_angle: 旋转角度
    :return: None
    """
    # 打开PDF文件
    pdf = fitz.open(pdfPath)
    name = os.path.basename(pdfPath).replace('.pdf', '')
    # 逐页读取PDF
    for pg in range(0, pdf.pageCount):
        page = pdf[pg]
        # 设置缩放和旋转系数
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
        pm = page.getPixmap(matrix=trans, alpha=False)
        # 开始写图像
        if imgPath is None:
            imgPath = os.path.dirname(pdfPath) + '/'+name
            os.makedirs(imgPath, exist_ok=True)
        pm.writePNG(imgPath + '/' + name + '_' + str(pg + 1).rjust(5, '0') + ".jpg")
    pdf.close()


def one_hot(pdf_path, bright=1.0, contrast=1.0, color=1.0, sharpness=1.0, saveFolderPath=None, zoom=1):
    pdf_image(pdf_path, zoom, zoom)
    image_path = os.path.dirname(pdf_path) + '/' + os.path.basename(pdf_path).replace('.pdf', '')
    files = os.listdir(image_path)
    for file in files:
        if 'png' in file or 'jpg' in file:
            image_enhance(image_path + '/'+file, bright, contrast, color, sharpness, saveFolderPath)
    enhance_image_path = os.path.dirname(pdf_path) + '/' + os.path.basename(pdf_path).replace('.pdf', '') + '/enhance/'
    combine_imgs_pdf(enhance_image_path, os.path.dirname(pdf_path) + '/' + os.path.basename(pdf_path).replace('.pdf', '_enhance.pdf'))
    # for root, dirs, files in os.walk(image_path, topdown=False):
    #     for name in files:
    #         os.remove(os.path.join(root, name))
    #     for name in dirs:
    #         os.rmdir(os.path.join(root, name))
    # os.rmdir(image_path)



if __name__ == '__main__':
    one_hot(r'E:\Code\Python\csdn\image\强化学习（第2版）.pdf', 1.3, 1.5, 1.3, 1.0, zoom=4)
    # pp = r'E:\Code\Python\csdn\image\机器学习 .jpg'
    # image_enhance(pp, 1.0, 1.5, 1.5, 1.0)
    # combine_imgs_pdf('E:\Code\Python\csdn\image\机器学习/', 'E:\Code\Python\csdn/1.pdf')
