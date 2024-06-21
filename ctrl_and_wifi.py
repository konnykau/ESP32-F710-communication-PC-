import socket
from inputs import get_gamepad

def main():
    ip_address = '192.168.11.4' #サーバー（ESP32のIPアドレス）
    port = 5000 #ポート番号
    buffer_size = 4092 #一度に受け取るデータの大きさを指定
    #クライアント用インスタンスを生成
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # サーバーに接続を要求する（IPアドレスとポート番号を指定）
    client.connect((ip_address, port))
    # サーバにデータを送信する
    try:
        print(str,"connected")
        while True:
            events = get_gamepad()
            for event in events:
                if event.ev_type != "Sync" :
                    client.sendall(bytes(event.code + "\n", encoding='ASCII'))
                    client.sendall(bytes(str(event.state) + "\n", encoding='ASCII'))


                # if event.code == "BTN_WEST":
                #     client.sendall(b"1")
                #     client.sendall(bytes(event.state))
                # elif event.code == "BTN_NORTH":
                #         client.sendall(bytes(0b1))
                #         client.sendall(bytes(event.state))
                # elif event.code == "BTN_SOUTH":
                #         client.sendall(bytes(0b01000000))
                #         client.sendall(bytes(event.state))
                # elif event.code == "BTN_EAST":
                #         client.sendall(bytes(0b00000011))
                #         client.sendall(bytes(event.state))
                # elif event.code == "BTN_TR":
                #         client.sendall(bytes(0b00000100))
                #         client.sendall(bytes(event.state))
                # elif event.code == "BTN_TL":
                #         client.sendall(bytes(0b00000101))
                #         client.sendall(bytes(event.state))
                # elif event.code == "BTN_SELECT":
                #         client.sendall(bytes(0b00000110))
                #         client.sendall(bytes(event.state))
                # elif event.code == "BTN_START":
                #         client.sendall(bytes(0b00000111))
                #         client.sendall(bytes(event.state))
                # elif event.code == "ABS_X":
                #         client.sendall(bytes(0b00001000))
                #         client.sendall(bytes(event.state // 256))
                # elif event.code == "ABS_Y":
                #         client.sendall(bytes(0b00001001))
                #         client.sendall(bytes(event.state // 256))
                # elif event.code == "ABS_RX":
                #         client.sendall(bytes(0b00001010))
                #         client.sendall(bytes(event.state // 256))
                # elif event.code == "ABS_RY":
                #         client.sendall(bytes(0b00001011))
                #         client.sendall(bytes(event.state // 256))
                # elif event.code == "ABS_HAT0X":
                #         client.sendall(bytes(0b00001100))
                #         client.sendall(bytes(event.state))
                # elif event.code == "ABS_HAT0Y":
                #         client.sendall(bytes(0b00001101))
                #         client.sendall(bytes(event.state))
                # elif event.code == "ABS_RZ":
                #         client.sendall(bytes(0b00001110))
                #         client.sendall(bytes(event.state))
                # elif event.code == "ABS_Z":
                #         client.sendall(bytes(0b00001111))
                #         client.sendall(bytes(event.state))    



    except KeyboardInterrupt:
        client.close()
        print("プログラムを終了します。")

if __name__ == "__main__":
    main()