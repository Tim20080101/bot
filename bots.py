# bots.py

import os
import subprocess
import time
import sys
from dotenv import load_dotenv
load_dotenv() # 在程式碼最開始載入 .env 檔案中的變數

# 定義環境變數名稱，而不是 Token 本身！
HELLOBOT_TOKEN_KEY = 'HELLOBOT_TOKEN'
MATHBOT_TOKEN_KEY = 'MATHBOT_TOKEN'

BOT_SCRIPTS = [
    "hellobot.py",
    "mathbot.py"
]

def run_bots():
    
    # 檢查 Token 是否存在於環境變數中
    hello_token = os.getenv(HELLOBOT_TOKEN_KEY)
    math_token = os.getenv(MATHBOT_TOKEN_KEY)
    
    if not hello_token or not math_token:
        print("❌ 錯誤：啟動機器人所需的環境變數未設定。")
        print(f"請確保設定了 {HELLOBOT_TOKEN_KEY} 和 {MATHBOT_TOKEN_KEY}。")
        sys.exit(1) # 程式退出

    processes = []
    print("--- 啟動 Discord 機器人 ---")

    # 由於您的 hellobot.py 和 mathbot.py 也會讀取相同的環境變數
    # 所以這裡不需要特別傳遞 Token 給子程序，它們會繼承父程序的環境變數。
    
    # ... (後續的 subprocess.Popen 邏輯保持不變)

    for script in BOT_SCRIPTS:
        try:
            # Popen 會繼承當前環境變數
            process = subprocess.Popen([sys.executable, "-u", script])
            processes.append(process)
            print(f"✅ 成功啟動 {script} (PID: {process.pid})")
            time.sleep(1)
        except Exception as e:
            print(f"❌ 啟動 {script} 時發生錯誤: {e}")

    print("\n所有機器人已在背景運行。按下 Ctrl+C 停止它們。\n")
    
    try:
        # 主程序等待所有子程序結束
        # 如果子程序是 Discord 機器人，它們會持續運行
        # 這是一個阻塞呼叫，讓主程序保持開啟
        while True:
            # 檢查是否有子程序已經結束
            for process in processes:
                if process.poll() is not None:
                    # 如果機器人意外停止，可以考慮在這裡加入重啟邏輯
                    print(f"⚠️ {BOT_SCRIPTS[processes.index(process)]} 意外停止。")
                    # 為了這個範例的簡單性，我們只退出循環
                    raise KeyboardInterrupt
            
            time.sleep(5) # 每 5 秒檢查一次
            
    except KeyboardInterrupt:
        print("\n--- 接收到停止指令 (Ctrl+C)，正在關閉機器人 ---")
        
        # 逐一終止所有子程序
        for script, process in zip(BOT_SCRIPTS, processes):
            if process.poll() is None: # 只有在程序還在運行時才終止
                print(f"🔪 正在終止 {script}...")
                process.terminate() # 嘗試溫和地終止
        
        # 給程序一點時間終止
        time.sleep(3) 

        # 檢查是否還有程序未終止，如果是則強制殺死
        for script, process in zip(BOT_SCRIPTS, processes):
            if process.poll() is None:
                print(f"💀 {script} 未回應，強制殺死...")
                process.kill()
                
        print("所有機器人已關閉。程式結束。")

if __name__ == "__main__":
    run_bots()