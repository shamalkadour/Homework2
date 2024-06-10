import socket
import threading
import time

host = 'localhost'  # عنوان المضيف
port = 11111  # رقم المنفذ
accounts = {
    "123456789": {"balance": 1000, "pin": 1234},
    "987654321": {"balance": 5000, "pin": 4321},
}

def handle_client(client_socket):
    for a in accounts.keys():
            client_socket.send(a.encode())
            # استقبال البيانات من العميل
            data = client_socket.recv(1024).decode().strip()


            # تحليل البيانات وتنفيذ الطلب
            request = data.split()
            command = request[0]        
            account_number = request[1]
            pin = request[2] if len(request) > 2 else None

            if command == "check_balance":
                if verify_account(account_number, pin):
                   response = f"Your balance is: {accounts[account_number]['balance']:.2f}"
                else:
                    response = "Invalid account number or PIN."

            elif command == "deposit":
                    amount = float(request[3])
                    if verify_account(account_number, pin):
                        accounts[account_number]["balance"] += amount
                        response = f"Deposited {amount:.2f}. Your new balance is: {accounts[account_number]['balance']:.2f}"
                    else:
                        response = "Invalid account number or PIN."

            elif command == "withdraw":
                    amount = float(request[3])
                    if verify_account(account_number, pin) and accounts[account_number]["balance"] >= amount:
                        accounts[account_number]["balance"] -= amount
                        response = f"Withdrawn {amount:.2f}. Your new balance is: {accounts[account_number]['balance']:.2f}"
                    else:
                        response = "Insufficient funds."

            else:
                response = "Invalid command."

            # إرسال الاستجابة إلى العميل
            client_socket.sendall(response.encode("utf-8"))
            

    # إغلاق اتصال العميل
    client_socket.close()

def verify_account(account_number, pin):
    if account_number not in accounts:
        return False
    if pin is None or accounts[account_number]["pin"] != pin:
        return False
    return True

def start_server():
    server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 11111))
    server_socket.listen(5)  # عدد اتصالات العملاء المسموح بها في قائمة الانتظار

    while True:
        client_socket, address = server_socket.accept()
        print(f"[INFO] Connected to {address}")

            # إنشاء خيط جديد لكل عميل
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    print("[INFO] Starting server...")
    start_server()
