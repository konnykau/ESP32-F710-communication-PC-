import socket
from inputs import get_gamepad
import re
import json
from pathlib import Path

def input_ip_address():
    ip_address = ''

    ip_address_pattern = '^192\.168\.11\.\d{1,3}$'

    while True:
        ip_address = input('Input the IP address of your ESP32 >> ')
        if re.match(ip_address_pattern, ip_address) is None:
            print(f'Invalied IP address: {ip_address}')
            continue
        else:
            break

    return ip_address

def input_port_num():
    port = 5000

    while True:
        port_str = input(f'Input the port number (input no character to set to default configuration: {port}) >> ')
        if port_str == '':
            break
        elif re.match('^\d+$', port_str):
            port = int(port_str)
            break
        else:
            print(f'Invalied port number: {port_str}')
            continue

    return port

def input_buffer_size():
    buffer_size = 4092

    while True:
        buffer_size_str = input(f'Input the buffer size (input no character to set to default configuration: {buffer_size}) >> ')
        if buffer_size_str == '':
            break
        elif re.match('^\d+$', buffer_size_str):
            buffer_size = int(buffer_size_str)
            break
        else:
            print(f'Invalied buffer size: {buffer_size_str}')
            continue

    return buffer_size

def load_config():
    path_to_config_file = Path(__file__).parents[0] / 'config.json'

    config = None

    if not path_to_config_file.exists():
        print(f'Config file: {str(path_to_config_file)} is not found. Begin configuration procedure.')
        config = {}
        config['ip_address'] = input_ip_address()
        config['port'] = input_port_num()
        config['buffer_size'] = input_buffer_size()

        with open(path_to_config_file, 'w') as f:
            json.dump(config, f)
        
    else:
        print(f'Config file: {str(path_to_config_file)} is found.')
        print('If you want to reset configuration, delete the config file.')
        with open(path_to_config_file) as f:
            config = json.load(f)
        
        if not ('ip_address' in config and type(config['ip_address']) is str and re.match('^192\.168\.11\.\d{1,3}$', config['ip_address']) is not None):
            print('The config file is broken! Delete the config file and restart this program: error 1')
            return None
        if not ('port' in config and type(config['port']) is int):
            print('The config file is broken! Delete the config file and restart this program: error 2')
            return None
        if not ('buffer_size' in config and type(config['buffer_size']) is int):
            print('The config file is broken! Delete the config file and restart this program: error 3')
            return None
    
    print('Applied configuration:')
    print(f'\tIP address: {config["ip_address"]}')
    print(f'\tPort number: {config["port"]}')
    print(f'\tBuffer size: {config["buffer_size"]}')
    
    return config

def main():
    config = load_config()
    if config is None:
        exit()

    #ip_address = '192.168.11.4' #サーバー（ESP32のIPアドレス）
    ip_address = config['ip_address'] #サーバー（ESP32のIPアドレス）
    port = config['port'] #ポート番号
    buffer_size = config['buffer_size'] #一度に受け取るデータの大きさを指定
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

 



    except KeyboardInterrupt:
        client.close()
        print("プログラムを終了します。")

if __name__ == "__main__":
    main()