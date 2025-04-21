from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

app = Flask(__name__)

DB_FILE = "price.db"

ITEM_GROUPS = {
    "素材類": ["鳥類翅膀", "花蜜", "惡夢結晶", "牛王的皮", "防裂化劑", "四葉首蓿草", "豪華皮革", "牛津布", "秘銀礦石", "魔兔魂"],
    "技能書類": ["舞者之書", "魔法戰士之書", "暗黑之書", "吟遊詩人之書", "忍之書", "徒手戰鬥之書"],
    "回復藥劑類": ["回復劑V", "回復劑VI", "回復劑VII"],
    "道具類": ["無敵神速飲料", "神速魔壺", "穿甲油", "澎湃藥丸", "障壁解析石板", "魔導師的秘藥", "銀杏炊飯", "金黃栗子泥"]
}

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                商品 TEXT,
                數量 INTEGER,
                價格 INTEGER,
                備註 TEXT,
                時間 TEXT
            )
        """)
        conn.commit()

@app.route("/")
def index():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM price_history ORDER BY 時間 DESC")
    records = cursor.fetchall()
    conn.close()
    return render_template("index.html", item_groups=ITEM_GROUPS, records=records)

@app.route("/add", methods=["POST"])
def add():
    item = request.form["item"]
    quantity = request.form["quantity"]
    price = request.form["price"]
    note = request.form["note"]
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        quantity = int(quantity)
        price = int(price.replace(",", ""))
    except:
        return redirect("/")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO price_history (商品, 數量, 價格, 備註, 時間) VALUES (?, ?, ?, ?, ?)",
                   (item, quantity, price, note, now))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM price_history WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
