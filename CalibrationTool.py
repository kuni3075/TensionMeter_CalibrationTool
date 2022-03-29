from concurrent.futures import thread
import tkinter as tk
import tkinter.ttk as ttk
from typing import Text
import threading
import function as f

# 関数定義
def button1_click():
    start_text.set("測定中")
    thread1 = threading.Thread(target=f.measureProcess)
    thread1.start()
    thread1.join()
    start_text.set("測定開始")

# フレームの作成
root = tk.Tk()
root.title("張力計キャリブレーションソフト")
frame1 = tk.Frame()
frame2 = tk.Frame()

# フレームの設定
frame1.grid()
frame2.grid()

# 変数定義
start_text = tk.StringVar(frame1)
start_text.set("測定開始")

# ===============================================================
# frame1
# ビューの定義と設定
label1 = ttk.Label(frame1, text="使用する重り")
label2 = ttk.Label(frame1, text="kg")
entry1 = ttk.Entry(frame1)
button1 = ttk.Button(frame1, textvariable=start_text, command=button1_click)

# ビューの配置
label1.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)
entry1.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5)
label2.grid(row=0, column=2, padx=0, pady=5, ipadx=5, ipady=5)
button1.grid(row=0, column=3, padx=10, pady=5, ipadx=5, ipady=5)

# ===============================================================
# frame2

# ツリービューの作成
tree = ttk.Treeview(frame2)
# 列インデックスの作成
tree["columns"] = (1,2,3,4)
# 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
tree["show"] = "headings"
# 各列の設定(インデックス,オプション(今回は幅を指定))
tree.column(1)
tree.column(2)
tree.column(3)
tree.column(4)
# 各列のヘッダー設定(インデックス,テキスト)
tree.heading(1,text="重り")
tree.heading(2,text="デジタル値")
tree.heading(3,text="測定値")
tree.heading(4,text="データ数")

# レコードの追加
# 1番目の引数-配置場所（ツリー形式にしない表設定ではブランクとする）
# 2番目の引数-end:表の配置順序を最下部に配置
#             (行インデックス番号を指定することもできる)
# 3番目の引数-values:レコードの値をタプルで指定する
tree.insert("","end",values=("2017/5/1","食費",3500))
tree.insert("","end",values=("2017/5/10","光熱費",7800))
tree.insert("","end",values=("2017/5/10","住宅費",64000))

# ===============================================================

tree.grid(row=0,column=0, padx=5, pady=5, ipadx=5, ipady=5)

root.mainloop()