import tkinter as tk
import tkinter.ttk as ttk
from turtle import shape
import serial
from serial.tools import list_ports
import threading
import numpy as np

# 変数定義
measure_flag = False
send_flag = False
comport = ""
weight = 0
value = 0


# ===============================================================
# 関数 GUI
def button1_click():
    global measure_flag
    
    button1_text.set("測定中")
    button1.state(['pressed'])
    button1.state(['disabled'])
    measure_flag = True
    
def button2_click():
    global send_flag
    
    button2_text.set("送信中")
    button2.state(['pressed'])
    button2.state(['disabled'])
    send_flag = True

def button3_click():
    id = tree.focus()
    tree.delete(id)

def button4_click():
    cnt = len(tree.get_children())
    data = np.zeros([cnt,3])
    for i,id in enumerate(tree.get_children()):
        a = list(tree.item(id, "values"))
        for j in range(3):
            if a[j] == "":
                a[j] = "0"
            data[i][j] = float(a[j])
    x = data[:,1]
    y = data[:,0]
    b = np.dot(x, y)/ (x ** 2).sum()
    entry2.delete(0,len(entry2.get()))
    entry2.insert(0,str(b))

def button5_click():
    with open('Proofread.txt','r') as f:
        entry2_text.set(f.readline())
    
def SubLoop():
    global measure_flag
    global send_flag
    global comport
    
    while True:
        # 接続先の更新
        # 取得したポートのリストをinfoに代入し、descriptionを実行して返す(リスト内包表記)
        combobox1["values"] = [info.description for info in list_ports.comports()]
        ports = [info.device for info in list_ports.comports()]
        comport = ports[combobox1.current()]
        
        # 補正値の計算
        
        
        # ボタンを押したときの処理
        if measure_flag:
            MeasureProcess()
            measure_flag = False
            button1.state(['!disabled'])
            button1.state(['!pressed'])
            button1_text.set("測定開始")
        elif send_flag:
            SendProcess()
            send_flag = False
            button2.state(['!disabled'])
            button2.state(['!pressed'])
            button2_text.set("送信")
        else:
            label6_text.set("")

# ===============================================================
# 関数 測定

def MeasureProcess():
    var = []
    var_str = ""
    var_ok_ng = ""
    ser = serial.Serial(comport, 115200, timeout=0.5)
    ser.write(str.encode("2,2\r\n"))
    ser.reset_input_buffer()
    
    if ser.readline().decode() == "Calibration Mode\r\n":
        for i in range(20):
            var_str = ser.readline()
            var.append(float(var_str.decode().rstrip()))
            label6_text.set(str(i*5) + "%")
        var_avg = np.mean(var)
        var_stdev = np.std(var)
        if var_stdev < 200 and var_stdev > -200:
            var_ok_ng = "OK"
        else:
            var_ok_ng = "再測定"
        tree.insert("","end",values=(entry1.get(),var_avg,var_stdev,var_ok_ng))
    else:
        tree.insert("","end",values=("","","通信エラー"))
    ser.write(str.encode("2,0\r\n"))
    ser.close()
    
def SendProcess():
    ser = serial.Serial(comport, 115200, timeout=0.5)
    ser.reset_input_buffer()
    ser.write(str.encode("1," + str(entry2_text.get())))
    
    read_str1 = ser.readline().decode()
    read_str2 = ser.readline().decode()
    if read_str1 == "Proofread Update\r\n":
        label5_text.set(read_str2 + "送信完了")
        with open('Proofread.txt','w') as f:
            f.write(str(entry2_text.get()))
    else:
        label5_text.set("通信エラー")
    ser.close()

# ===============================================================
# フレームの作成
root = tk.Tk()
root.title("張力計キャリブレーションソフト ver1.0")
root.grid()
frame1 = ttk.Frame(relief='raised')
frame2 = ttk.Frame(relief='raised')
frame3 = ttk.Frame(relief='raised')
frame4 = ttk.Frame(relief='raised')

# フレームの設定
frame1.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)
frame2.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5)
frame3.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=5)
frame4.grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=5)

# ===============================================================
# ビューの作成

# frame1
label1 = ttk.Label(frame1, text="接続先")
combobox1 = ttk.Combobox(frame1, width=40, state="readonly", values=[])


# frame2
button1_text = tk.StringVar(frame2)
button1_text.set("測定開始")
label6_text = tk.StringVar(frame2)
label6_text.set("")

label2 = ttk.Label(frame2, text="使用する重り")
label3 = ttk.Label(frame2, text="kg")
label6 = ttk.Label(frame2, textvariable=label6_text)
entry1 = ttk.Entry(frame2)
button1 = ttk.Button(frame2, textvariable=button1_text, command=button1_click)

# frame3
button3 = ttk.Button(frame3, text="選択したデータの削除", command=button3_click)

# ツリービューの作成
tree = ttk.Treeview(frame3)
# 列インデックスの作成
tree["columns"] = (1,2,3,4)
# 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
tree["show"] = "headings"
# 各列の設定(インデックス,オプション(今回は幅を指定))
tree.column(1,width=75)
tree.column(2,width=75)
tree.column(3,width=75)
tree.column(4,width=75)
# 各列のヘッダー設定(インデックス,テキスト)
tree.heading(1,text="重り")
tree.heading(2,text="平均値")
tree.heading(3,text="標準偏差")
tree.heading(4,text="判定")

# レコードの追加
# 1番目の引数-配置場所（ツリー形式にしない表設定ではブランクとする）
# 2番目の引数-end:表の配置順序を最下部に配置
#             (行インデックス番号を指定することもできる)
# 3番目の引数-values:レコードの値をタプルで指定する

# frame4
label5_text = tk.StringVar(frame4)
label5_text.set("")
button2_text = tk.StringVar(frame4)
button2_text.set("送信")
entry2_text = tk.StringVar(frame4)
label4 = ttk.Label(frame4, text="補正値")
label5 = ttk.Label(frame4, textvariable=label5_text)
entry2 = ttk.Entry(frame4, textvariable=entry2_text)
button2 = ttk.Button(frame4, textvariable=button2_text, command=button2_click)
button4 = ttk.Button(frame4, text="更新", command=button4_click)
button5 = ttk.Button(frame4, text="前回の\n補正値", command=button5_click)

# ===============================================================
# ビューの配置
# farme1
label1.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)
combobox1.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5)

# frame2
label2.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)
entry1.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5)
label3.grid(row=0, column=2, padx=0, pady=5, ipadx=5, ipady=5)
button1.grid(row=1, column=1, padx=10, pady=5, ipadx=5, ipady=5)
label6.grid(row=1, column=2, padx=10, pady=5, ipadx=5, ipady=5)

# frame3
tree.grid(row=0,column=0, padx=5, pady=5, ipadx=5, ipady=5)
button3.grid(row=1,column=0, padx=5, pady=5, ipadx=5, ipady=5)

#frame4
label4.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)

entry2.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5)
button4.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=5)
button5.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5)
label5.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5)
button2.grid(row=1, column=2, padx=5, pady=5, ipadx=5, ipady=5)

# ===============================================================

# スレッドの設定とスタート
# スレッドはデーモンスレッド(メインルーチンが終了したら強制終了するスレッド)に設定
thread1 = threading.Thread(target=SubLoop)
thread1.setDaemon(True)
thread1.start()

root.mainloop()