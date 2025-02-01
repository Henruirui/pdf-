import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import os

# 设置 Tesseract 路径（根据你的安装路径进行修改）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class Separator(tk.Frame):
    def __init__(self, master=None, orientation="horizontal", cursor="sb_v_double_arrow"):
        super().__init__(master)
        self.orientation = orientation
        self.cursor = cursor
        if orientation == "vertical":
            self.config(width=5, relief=tk.RAISED, bd=1, cursor=cursor)
        elif orientation == "horizontal":
            self.config(height=5, relief=tk.RAISED, bd=1, cursor=cursor)


class PDFViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF OCR 查看器")
        self.root.geometry("1200x800")

        # 创建主框架
        main_frame = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=5)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # 创建左侧面板（PDF页面显示）
        self.left_panel = tk.Frame(main_frame, bg='lightgray')
        main_frame.add(self.left_panel, width=600)

        # 创建右侧面板（OCR文本显示）
        self.right_panel = tk.Frame(main_frame, bg='white')
        main_frame.add(self.right_panel, width=600)

        # 左侧面板：PDF页面显示
        self.image_canvas = tk.Canvas(self.left_panel, bg='white')
        self.image_canvas.pack(expand=True, fill=tk.BOTH)

        # 添加滚动条
        h_scrollbar = tk.Scrollbar(self.left_panel, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
        v_scrollbar = tk.Scrollbar(self.left_panel, orient=tk.VERTICAL, command=self.image_canvas.yview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.image_canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

        # 右侧面板：OCR文本显示
        self.text_display = tk.Text(self.right_panel, wrap=tk.WORD)
        self.text_display.pack(expand=True, fill=tk.BOTH)

        # 控制面板
        control_panel = tk.Frame(self.root)
        control_panel.pack(fill=tk.X)

        self.load_button = tk.Button(control_panel, text="加载 PDF", command=self.load_pdf)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.ocr_button = tk.Button(control_panel, text="执行 OCR", command=self.perform_ocr)
        self.ocr_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.prev_page_button = tk.Button(control_panel, text="上一页", command=self.prev_page)
        self.prev_page_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.next_page_button = tk.Button(control_panel, text="下一页", command=self.next_page)
        self.next_page_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.reset_zoom_button = tk.Button(control_panel, text="还原缩放", command=self.reset_zoom)
        self.reset_zoom_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.pdf_document = None
        self.current_page = 0
        self.photo = None
        self.zoom_factor = 1.0
        self.original_image = None
        self.scroll_offset_x = 0
        self.scroll_offset_y = 0
        self.drag_start_x = 0
        self.dragging = False

        # 绑定鼠标事件
        self.image_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.image_canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.image_canvas.bind("<B1-Motion>", self.on_move)
        self.image_canvas.bind("<ButtonRelease-1>", self.on_release)

    def load_pdf(self):
        """加载 PDF 文件"""
        file_path = filedialog.askopenfilename(filetypes=[("PDF 文件", "*.pdf")])  # 打开文件对话框选择 PDF 文件
        if file_path:
            try:
                self.pdf_document = fitz.open(file_path)  # 打开 PDF 文件
                self.current_page = 0  # 初始化为第一页
                self.display_page()  # 显示第一页
                messagebox.showinfo("成功", "PDF 加载成功！")  # 显示成功消息
            except Exception as e:
                messagebox.showerror("错误", f"加载 PDF 失败: {e}")  # 显示错误消息

    def display_page(self):
        """显示当前 PDF 页面"""
        if not self.pdf_document:
            return

        page = self.pdf_document[self.current_page]  # 获取当前页
        pix = page.get_pixmap(dpi=300)  # 获取页面图像，DPI 设置为 300 提高图像质量
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # 将图像转换为 Pillow 图像对象

        # 预处理图像
        preprocessed_img = self.preprocess_image(img)

        self.original_image = preprocessed_img.copy()  # 保存原始图像
        self.zoom_factor = 1.0  # 重置缩放因子
        self.scroll_offset_x = 0  # 重置水平滚动偏移量
        self.scroll_offset_y = 0  # 重置垂直滚动偏移量
        self.fit_to_canvas()  # 调整图像大小以适应画布
        self.update_image()  # 更新显示的图像

    def preprocess_image(self, img):
        """预处理图像以提高 OCR 准确性"""
        # 去噪
        img = img.filter(ImageFilter.MedianFilter())  # 使用中值滤波去噪

        # 增强对比度
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)  # 增强对比度

        # 转换为灰度图像
        img = img.convert('L')  # 转换为灰度图像

        # 应用阈值二值化
        threshold = 128
        img = img.point(lambda p: p > threshold and 255)  # 应用阈值二值化

        return img

    def perform_ocr(self):
        """执行 OCR 识别当前页面"""
        if not self.pdf_document:
            messagebox.showwarning("警告", "请先加载一个 PDF 文件。")  # 显示警告消息
            return

        page = self.pdf_document[self.current_page]  # 获取当前页
        pix = page.get_pixmap(dpi=300)  # 获取页面图像，DPI 设置为 300 提高图像质量
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # 将图像转换为 Pillow 图像对象

        # 预处理图像
        preprocessed_img = self.preprocess_image(img)

        try:
            # 使用 Tesseract 进行 OCR，设置 Page Segmentation Mode (PSM) 为 1（自动分段，带OSD）
            custom_config = r'--oem 3 --psm 1'

            # 多语言支持，同时支持中文和英文
            text = pytesseract.image_to_string(preprocessed_img, lang='chi_sim+eng', config=custom_config)
            self.text_display.delete(1.0, tk.END)  # 清空文本显示区域
            self.text_display.insert(tk.END, text)  # 插入识别结果
        except pytesseract.pytesseract.TesseractError as e:
            messagebox.showerror("Tesseract 错误", f"Tesseract 错误在第 {self.current_page + 1} 页: {e}")  # 显示错误消息
        except Exception as e:
            messagebox.showerror("错误", f"第 {self.current_page + 1} 页发生错误: {e}")  # 显示错误消息

    def prev_page(self):
        """切换到上一页"""
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1  # 切换到上一页
            self.display_page()  # 显示上一页
            self.perform_ocr()  # 执行 OCR

    def next_page(self):
        """切换到下一页"""
        if self.pdf_document and self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1  # 切换到下一页
            self.display_page()  # 显示下一页
            self.perform_ocr()  # 执行 OCR

    def reset_zoom(self):
        """还原图像缩放"""
        self.zoom_factor = 1.0  # 重置缩放因子
        self.scroll_offset_x = 0  # 重置水平滚动偏移量
        self.scroll_offset_y = 0  # 重置垂直滚动偏移量
        self.fit_to_canvas()  # 调整图像大小以适应画布
        self.update_image()  # 更新显示的图像

    def fit_to_canvas(self):
        """调整图像大小以适应画布"""
        if self.original_image is None:
            return

        canvas_width = self.image_canvas.winfo_width()  # 获取画布宽度
        canvas_height = self.image_canvas.winfo_height()  # 获取画布高度

        img_width = self.original_image.width
        img_height = self.original_image.height

        # 计算缩放因子以适应画布
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        self.zoom_factor = min(scale_x, scale_y)  # 选择较小的缩放因子以确保图像完全可见

    def update_image(self):
        """更新显示的图像"""
        if self.original_image is None:
            return

        new_width = int(self.original_image.width * self.zoom_factor)  # 计算新的宽度
        new_height = int(self.original_image.height * self.zoom_factor)  # 计算新的高度
        resized_photo = ImageTk.PhotoImage(self.original_image.resize((new_width, new_height)))  # 调整图像大小

        self.image_canvas.delete("all")  # 清除画布上的所有内容
        self.image_canvas.create_image(self.scroll_offset_x, self.scroll_offset_y, anchor=tk.NW,
                                       image=resized_photo)  # 显示调整后的图像
        self.image_canvas.config(scrollregion=(0, 0, new_width, new_height))  # 设置滚动区域
        self.photo = resized_photo  # 保存图像对象

    def on_mousewheel(self, event):
        """处理鼠标滚轮事件以缩放图像"""
        if self.original_image is None:
            return

        scale = 1.1 if event.delta > 0 else 0.9  # 根据滚轮方向设置缩放比例
        canvas_center_x = self.image_canvas.canvasx(event.x)  # 计算画布中心 x 坐标
        canvas_center_y = self.image_canvas.canvasy(event.y)  # 计算画布中心 y 坐标

        # 设置缩放因子限制
        min_zoom = 0.1
        max_zoom = 10.0

        old_zoom_factor = self.zoom_factor
        new_zoom_factor = self.zoom_factor * scale

        if new_zoom_factor < min_zoom or new_zoom_factor > max_zoom:
            return

        self.zoom_factor = new_zoom_factor

        # 计算滚动偏移量以保持鼠标位置居中
        delta_x = (canvas_center_x - self.scroll_offset_x) * (scale - 1)
        delta_y = (canvas_center_y - self.scroll_offset_y) * (scale - 1)

        self.scroll_offset_x -= delta_x
        self.scroll_offset_y -= delta_y

        self.update_image()  # 更新显示的图像

    def on_button_press(self, event):
        """处理鼠标按下事件以开始拖动"""
        self.drag_start_x = event.x  # 记录拖动开始位置 x
        self.drag_start_y = event.y  # 记录拖动开始位置 y
        self.dragging = True  # 开始拖动

    def on_move(self, event):
        """处理鼠标移动事件以拖动图像"""
        if not self.dragging:
            return

        dx = event.x - self.drag_start_x  # 计算 x 方向的位移
        dy = event.y - self.drag_start_y  # 计算 y 方向的位移
        self.scroll_offset_x += dx  # 更新水平滚动偏移量
        self.scroll_offset_y += dy  # 更新垂直滚动偏移量
        self.drag_start_x = event.x  # 更新拖动开始位置 x
        self.drag_start_y = event.y  # 更新拖动开始位置 y
        self.update_image()  # 更新显示的图像

    def on_release(self, event):
        """处理鼠标释放事件以结束拖动"""
        self.dragging = False  # 结束拖动


if __name__ == "__main__":
    root = tk.Tk()  # 创建主窗口
    app = PDFViewerApp(root)  # 创建应用实例
    root.mainloop()  # 运行主循环



