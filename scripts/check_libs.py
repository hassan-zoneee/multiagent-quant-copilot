import importlib

libraries_imports = ["fitz", "pdfplumber", "docx", "pytesseract", "bs4", "lxml", "PIL", "requests"]
for name in libraries_imports:
    try:
        importlib.import_module(name)
        print("ok ", name)
    except Exception as exce:  # noqa: BLE001
        print("failed ", name, exce)


try:
    import pytesseract
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (700, 120), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(size=40)
    draw.text((20, 30), "Test for Tesseract", fill="black", font=font)
    print("OCR result:", pytesseract.image_to_string(img).strip())
except Exception as exc:  # noqa: BLE001
    print("OCR test FAILED:", exc)
