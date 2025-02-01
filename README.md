当然可以！以下是一个关于你编写的 PDF OCR 查看器程序的简介：

---

# PDF OCR 查看器

## 简介

PDF OCR 查看器是一款功能强大的桌面应用程序，旨在帮助用户高效地查看和提取 PDF 文档中的文本内容。该程序结合了 `tkinter`、`Pillow`、`pytesseract` 和 `PyMuPDF`（fitz）等库，提供了友好的用户界面和丰富的功能。

## 主要功能

1. **加载 PDF 文件**:
   - 用户可以通过点击“加载 PDF”按钮选择并加载本地的 PDF 文件。
   - 支持多种格式的 PDF 文件，确保广泛的兼容性。

2. **执行 OCR 识别**:
   - 通过点击“执行 OCR”按钮，程序将对当前页面进行光学字符识别（OCR），并将识别出的文本显示在右侧面板中。
   - 支持多语言识别，包括中文和英文。

3. **页面导航**:
   - 用户可以通过“上一页”和“下一页”按钮轻松浏览 PDF 文档的不同页面。
   - 每次切换页面后，程序会自动重新执行 OCR 以更新文本显示。

4. **图像缩放与拖动**:
   - 用户可以使用鼠标滚轮来缩放 PDF 页面，以便更清晰地查看细节。
   - 通过拖动鼠标，用户可以在画布上平移图像，方便查看不同区域的内容。

5. **还原缩放**:
   - 点击“还原缩放”按钮，可以将 PDF 页面恢复到原始大小，便于整体浏览文档。

6. **分隔条调整**:
   - 使用可拖动的分隔条，用户可以根据需要调整左右两侧面板的宽度，从而更好地平衡图像显示和文本阅读的空间。

## 技术栈

- **Python**: 编程语言核心。
- **tkinter**: 提供图形用户界面（GUI）。
- **Pillow**: 图像处理库，用于预处理和显示 PDF 页面图像。
- **pytesseract**: 结合 Tesseract 引擎进行 OCR 识别。
- **PyMuPDF (fitz)**: 用于读取和处理 PDF 文件。

## 安装与运行

### 步骤 1: 安装 Python

1. **下载并安装 Python**:
   - 访问 [Python 官方网站](https://www.python.org/downloads/windows/) 下载最新版本的 Python。
   - 运行下载的安装程序，并确保勾选“Add Python to PATH”选项。
   - 按照提示完成安装过程。

### 步骤 2: 创建虚拟环境

1. **打开命令提示符**:
   - 按 `Win + R`，输入 `cmd` 并按回车键。

2. **导航到项目目录**:
   - 使用 `cd` 命令导航到你的项目目录：
     ```bash
     cd D:\pdf识别
     ```

3. **创建虚拟环境**:
   - 运行以下命令来创建虚拟环境：
     ```bash
     python -m venv .venv
     ```

4. **激活虚拟环境**:
   - 运行以下命令来激活虚拟环境：
     ```bash
     .venv\Scripts\activate
     ```

### 步骤 3: 安装必要的 Python 包

1. **安装所需的 Python 包**:
   - 使用 `pip` 安装必要的包：
     ```bash
     pip install tkinter pillow pytesseract pymupdf
     ```

### 步骤 4: 安装 Tesseract

1. **下载并安装 Tesseract**:
   - 访问 [Tesseract GitHub 发布页面](https://github.com/UB-Mannheim/tesseract/wiki) 下载适用于 Windows 的 Tesseract。
   - 运行下载的安装程序，并按照提示完成安装过程。

2. **配置 Tesseract 路径**:
   - 编辑你的 Python 脚本，在顶部添加 Tesseract 的路径：
     ```python
     import pytesseract
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```
   - 确保路径与你的 Tesseract 安装路径一致。

### 步骤 5: 下载训练数据

1. **检查已安装的语言数据**:
   - 打开命令提示符并运行以下命令查看已安装的语言数据：
     ```bash
     C:\Program Files\Tesseract-OCR\tesseract.exe --list-langs
     ```
   - 你应该会看到类似如下的输出：
     ```
     List of available languages in C:\Program Files\Tesseract-OCR\tessdata:
     eng
     chi_sim
     ```

2. **安装缺失的语言数据**:
   - 如果缺少中文或英文的数据，可以从 [Tesseract GitHub](https://github.com/tesseract-ocr/tessdata) 下载相应的 `.traineddata` 文件。
   - 例如，从 [Tesseract GitHub](https://github.com/tesseract-ocr/tessdata) 下载 `chi_sim.traineddata` 和 `eng.traineddata`。
   - 将下载的文件复制到 `C:\Program Files\Tesseract-OCR\tessdata` 目录下。

### 步骤 6: 运行应用程序

现在你可以运行你的 PDF OCR 查看器应用程序了。

1. **保存代码**:
   - 将上述代码保存为一个 Python 文件，例如 `pdf识别.py`。

2. **运行应用程序**:
   - 打开命令提示符并导航到保存文件的目录。
   - 确保虚拟环境已激活：
     ```bash
     .venv\Scripts\activate
     ```
   - 运行以下命令启动应用程序：
     ```bash
     python pdf识别.py
     ```

## 致谢

感谢开源社区提供的各种工具和技术支持，使得这款 PDF OCR 查看器得以实现。
