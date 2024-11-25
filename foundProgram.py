import pyautogui
import time
import os







def locate_image_on_screen(image_path, confidence=0.8, timeout=8):
    """
    在屏幕上查找图像的位置。
    :param image_path: 图像文件路径
    :param confidence: 图像匹配的置信度，默认为0.8
    :param timeout: 查找图像的超时秒数，默认为10秒
    :return: 如果找到图像，返回坐标元组 (left, top, width, height)；否则返回 None
    """
    # 检查图像文件是否存在
    if not os.path.exists(image_path):
        print(f"图像文件 {image_path} 不存在，请确保该图像文件在程序运行的目录中。")
        return None

    start_time = time.time()

    # 重试机制：超时后停止查找
    while time.time() - start_time < timeout:
        try:
            position = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if position:
                # 返回图像区域的坐标 (left, top, width, height)
                return position
        except pyautogui.ImageNotFoundException:
            continue
            # print(f"未找到图像 {image_path}，继续重试...")

        time.sleep(1)  # 每半秒检查一次

    print(f"未在 {timeout} 秒内找到图像 {image_path}.")
    return None