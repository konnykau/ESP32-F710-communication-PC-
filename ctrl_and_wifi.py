import socket
from inputs import get_gamepad

def main():
    ip_address = '192.168.32.100' #サーバー（ESP32のIPアドレス）
    port = 5000 #ポート番号
    buffer_size = 4092 #一度に受け取るデータの大きさを指定
    #クライアント用インスタンスを生成
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # サーバーに接続を要求する（IPアドレスとポート番号を指定）
    client.connect((ip_address, port))
    # サーバにデータを送信する
    try:
        while True: #無限ループ
            events = get_gamepad()#コントローラの入力を取得
            for event in events:
                if event.ev_type != "Sync" :
                    client.sendall(bytes(event.code + "\n", encoding='ASCII'))
                    client.sendall(bytes(str(event.state) + "\n", encoding='ASCII'))

    except KeyboardInterrupt:
        print("プログラムを終了します。")

if __name__ == "__main__":
    main()
