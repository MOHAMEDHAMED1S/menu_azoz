from flask import Flask, request, jsonify, send_from_directory
import os
import json
import webbrowser
import threading
import signal
# By Mohamed Hamed
app = Flask(__name__)
UPLOAD_FOLDER = "images"
JSON_FILE = "products.json"

# لو الملف مش موجود هينشئ واحد
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w") as f:
        json.dump([], f)

# تحميل الصور
@app.route('/images/<filename>')

def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# هنا بيحمل الاكلات من الملف
def load_products():
    with open(JSON_FILE, "r") as f:
        return json.load(f)

# دي داله حفظ  المنتجات
def save_products(products):
    with open(JSON_FILE, "w") as f:
        json.dump(products, f, indent=4)

# هنا بحدد الواجهه الاماميه
@app.route("/")
def index():
    return send_from_directory(".", "dashboard.html")

#هنا إضافة منتج جديد
@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.form
    file = request.files.get("image")
    if not all([data.get("name"), data.get("description"), data.get("price"), file]):
        return jsonify({"error": "جميع الحقول مطلوبة"}), 400

    # حفظ الصورة
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    # إضافة المنتج
    products = load_products()
    products.append({
        "name": data["name"],
        "description": data["description"],
        "price": float(data["price"]),
        "image": image_path
    })
    save_products(products)
    return jsonify({"message": "تم إضافة المنتج بنجاح"})

# الحصول على جميع المنتجات
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(load_products())

# تعديل منتج
@app.route("/edit_product/<int:product_id>", methods=["PUT"])
def edit_product(product_id):
    data = request.form
    file = request.files.get("image")
    products = load_products()

    if product_id >= len(products):
        return jsonify({"error": "المنتج غير موجود"}), 404

    # تحديث البيانات
    if data.get("name"):
        products[product_id]["name"] = data["name"]
    if data.get("description"):
        products[product_id]["description"] = data["description"]
    if data.get("price"):
        products[product_id]["price"] = float(data["price"])

    # تحديث الصورة إذا تم رفع صورة جديدة
    if file:
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)
        products[product_id]["image"] = f"/images/{file.filename}"

    save_products(products)
    return jsonify({"message": "تم تعديل المنتج بنجاح"})

# حذف منتج
@app.route("/delete_product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    products = load_products()

    if product_id >= len(products):
        return jsonify({"error": "المنتج غير موجود"}), 404

    products.pop(product_id)
    save_products(products)
    return jsonify({"message": "تم حذف المنتج بنجاح"})

# دي داله لفتح الموقع
def open_browser():
    url = "http://127.0.0.1:4400/"
    webbrowser.open(url)
    #دي داله اغلاق السيرفر
@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return 'تم إيقاف السيرفر بنجاح.'
# تشغيل الخادم في خيط منفصل
def run_server():
    app.run(host='0.0.0.0', port=4400,debug=True, use_reloader=False)  # use_reloader=False عشان الخادم ميشتغلش مرتين
# تشغيل الخادم وفتح المتصفح بعد بدء الخادم
if __name__ == "__main__":
    # تشغيل الخادم في خيط منفصل
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    # فتح المتصفح بعد تأكيد تشغيل الخادم
    open_browser()