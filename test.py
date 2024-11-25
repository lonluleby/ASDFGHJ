import numpy as np
import pyautogui
import time
import os
import cv2

class ImageLocator:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
    
    def basic_locate(self, image_path, confidence=0.8, timeout=8):
        """基础的图像查找方法"""
        if not os.path.exists(image_path):
            print(f"图像文件 {image_path} 不存在")
            return None

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                position = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if position:
                    return position
            except pyautogui.ImageNotFoundException:
                continue
            time.sleep(0.5)
        return None

    def locate_scaled_image(self, image_path, confidence=0.8, timeout=8, scale_range=(0.5, 1.5, 0.1)):
        """使用不同缩放比例查找图像"""
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法读取图像文件 {image_path}")
            return None
            
        start_time = time.time()
        
        for scale in np.arange(scale_range[0], scale_range[1], scale_range[2]):
            if time.time() - start_time > timeout:
                break
                
            # 缩放图像
            width = int(image.shape[1] * scale)
            height = int(image.shape[0] * scale)
            scaled_image = cv2.resize(image, (width, height))
            
            # 保存缩放后的图像
            temp_path = f"temp_scaled_{scale}.png"
            cv2.imwrite(temp_path, scaled_image)
            
            try:
                position = pyautogui.locateOnScreen(temp_path, confidence=confidence)
                os.remove(temp_path)
                if position:
                    return position
            except:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                continue
                
        return None

    def preprocess_image(self, image_path):
        """图像预处理"""
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法读取图像文件 {image_path}")
            return None
            
        # 转灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 增强对比度
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        # 保存处理后的图像
        processed_path = "processed_" + os.path.basename(image_path)
        cv2.imwrite(processed_path, enhanced)
        return processed_path

def locate_image_on_screen(image_path, confidence=0.8, timeout=8):
    """
    在屏幕上查找图像的位置。
    """
    # 检查图像文件是否存在
    if not os.path.exists(image_path):
        print(f"图像文件 {image_path} 不存在，请确保该图像文件在程序运行的目录中。")
        return None

    # 创建图像定位器实例
    locator = ImageLocator()
    start_time = time.time()

    while time.time() - start_time < timeout: 
        # 预处理图像
        processed_path = locator.preprocess_image(image_path)
        if processed_path:
            current_path = processed_path
        else:
            current_path = image_path

        # 方法1: 直接查找
        result = locator.basic_locate(current_path, confidence=0.5)
        if result:
            print("方法1成功：直接查找")
            # 清理预处理的临时文件
            if processed_path and os.path.exists(processed_path):
                os.remove(processed_path)
            return result

        # 方法2: 缩放查找
        result = locator.locate_scaled_image(current_path)
        if result:
            print("方法2成功：缩放查找")
            # 清理预处理的临时文件
            if processed_path and os.path.exists(processed_path):
                os.remove(processed_path)
            return result
        
        # 清理预处理的临时文件
        if processed_path and os.path.exists(processed_path):
            os.remove(processed_path)
        
        time.sleep(1)
    
    print(f"未在 {timeout} 秒内找到图像 {image_path}")
    return None

# 使用示例
if __name__ == "__main__":
    test_path = "test.png"
    result = locate_image_on_screen(test_path, confidence=0.7, timeout=3)
    if result:
        print(f"找到图像，位置：{result}")
    else:
        print("未找到图像")