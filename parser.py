import time
import threading
import vk  # Импортируем модуль vk
import platform
import os
import win10toast

online = ['не в сети', 'в сети']
status_code = ["вышел из сети", 'вошёл в сеть']
pref = 'https://vk.com/'
status = {}


def get_status_of_target(tok, ids):
    user_ids = '%s' % (','.join(map(str, ids)))
    users = {}
    data = vk_api.users.get(access_token=tok,
                            user_ids=user_ids, fields='online', name_case='Nom', v=5.89)
    for user in data:
        users[user['first_name'] + ' ' + user['last_name']] = user['online']

    return users


def check_status(tok, ids, base, fh):
    data = get_status_of_target(tok, ids)
    for i in data:
        if (i in base) and (base[i] != data[i]):
            push('VK-analyzer', i + ': ' + status_code[data[i]])
            fh.write(time.ctime(time.time()) + ' - ' + i + ': ' + status_code[data[i]] + '\n')
            fh.flush()
    return data


def push(title, message):
    plt = platform.system()
    if plt == "Darwin":
        command = '''
        osascript -e 'display notification "{message}" with title "{title}"'
        '''
    elif plt == "Linux":
        command = f'''
        notify-send "{title}" "{message}"
        '''
    elif plt == "Windows":
        win10toast.ToastNotifier().show_toast(title, message)
        return
    else:
        return
    os.system(command)

#      #####_MAIN_METHODS_#####


def stalking():
    t = open('targets.txt', 'r', encoding='UTF-8')
    users = []
    while True:
        line = t.readline()
        if not line:
            break
        users.append(line.replace(pref, '').replace('\n', ''))
    file_handler = open("output.txt", 'a', encoding='utf-8')
    print('Stalking starting')
    targets = get_status_of_target(token, users)
    message = ''
    for i in targets:
        message += i + ' : ' + online[targets[i]] + '\n'
    m = '*' * 20 + '\n' + time.ctime(time.time()) + '\n' + message + '*' * 20 + '\n'
    file_handler.write(m)
    file_handler.flush()
    push('VK-analyzer', message)
    while (status['stalking']):
        time.sleep(1)
        targets = check_status(token, users, targets, file_handler)
    print('Stalking aborted')


def something():
    return


class ThreadsMaker:
    def command_handler(self):
        threads = {}
        while(True):
            answer = str(input('> '))
            a = answer.split(' ')
            command = a[0]
            if command == 'stalking':
                subcommand = a[1]
                if subcommand == 'start':
                    th = threading.Thread(target=stalking, daemon=True)
                    th.start()
                    status['stalking'] = True
                    threads['stalking'] = th
                elif subcommand == 'stop':
                    status['stalking'] = False
            time.sleep(1)


if __name__ == "__main__":
    try:
        f = open('service_key.txt', 'r')
        token = str(f.readline())  # Сервисный ключ доступа
        f.close()
        session = vk.Session(access_token=token)  # Авторизация
        vk_api = vk.API(session)
        thread_master = ThreadsMaker()
        thread_master.command_handler()
    except FileNotFoundError:
        print('File \'service_key.txt\' not found!')





