from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Flask QR web đã chạy thành công ✅"
from flask import Flask, render_template_string, request
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer
)
from PIL import Image
import io, base64

app = Flask(__name__)

# HTML + CSS + JS (Bootstrap + Giao diện hiện đại)
HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>✨ Trình tạo mã QR cao cấp ✨</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body { background: linear-gradient(135deg, #6dd5fa, #ffffff); font-family: 'Segoe UI'; }
.card { border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
h1 { font-weight: bold; margin-top: 20px; color: #333; }
img { border-radius: 12px; margin-top: 20px; }
footer { margin-top: 30px; color: #555; }
</style>
</head>
<body>
<div class="container py-4">
  <h1 class="text-center mb-4">🌈 Trình Tạo Mã QR Code Cao Cấp</h1>
  <div class="card p-4">
    <form method="POST" enctype="multipart/form-data">
      <div class="mb-3">
        <label class="form-label">Nội dung hoặc URL:</label>
        <input type="text" name="data" class="form-control" placeholder="Nhập link hoặc văn bản..." required>
      </div>
      <div class="mb-3">
        <label class="form-label">Chọn màu QR:</label>
        <input type="color" name="fill_color" value="#000000">
        <label class="form-label ms-3">Màu nền:</label>
        <input type="color" name="back_color" value="#ffffff">
      </div>
      <div class="mb-3">
        <label class="form-label">Chọn kiểu QR:</label>
        <select class="form-select" name="style">
          <option value="square">Vuông</option>
          <option value="circle">Tròn</option>
          <option value="rounded">Bo góc</option>
          <option value="gapped">Dạng chấm</option>
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label">Tải logo (tùy chọn):</label>
        <input type="file" class="form-control" name="logo" accept="image/*">
      </div>
      <button class="btn btn-primary w-100">🚀 Tạo QR</button>
    </form>
  </div>

  {% if qr_code %}
  <div class="text-center mt-4">
    <h4>Mã QR của bạn:</h4>
    <img src="data:image/png;base64,{{ qr_code }}" width="250">
    <br>
    <a href="data:image/png;base64,{{ qr_code }}" download="qrcode.png" class="btn btn-success mt-3">📥 Tải về</a>
  </div>
  {% endif %}

  <footer class="text-center mt-5">
    van don
  </footer>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    qr_code = None
    if request.method == "POST":
        data = request.form["data"]
        fill_color = request.form.get("fill_color", "#000000")
        back_color = request.form.get("back_color", "#ffffff")
        style = request.form.get("style", "square")
        logo_file = request.files.get("logo")

        # Chọn kiểu module QR
        styles = {
            "square": SquareModuleDrawer(),
            "circle": CircleModuleDrawer(),
            "rounded": RoundedModuleDrawer(),
            "gapped": GappedSquareModuleDrawer()
        }
        module_style = styles.get(style, SquareModuleDrawer())

        # Tạo QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_style,
            color_mask=None,
            fill_color=fill_color,
            back_color=back_color
        ).convert("RGBA")

        # Thêm logo nếu có
        if logo_file and logo_file.filename != "":
            logo = Image.open(logo_file).convert("RGBA")
            logo.thumbnail((80, 80))
            pos = ((img.size[0] - logo.size[0]) // 2,
                   (img.size[1] - logo.size[1]) // 2)
            img.paste(logo, pos, logo)

        # Xuất ảnh base64
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_code = base64.b64encode(buf.getvalue()).decode("utf-8")

    return render_template_string(HTML, qr_code=qr_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)se64
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_code = base64.b64encode(buf.getvalue()).decode("utf-8")

    return render_template_string(HTML, qr_code=qr_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
