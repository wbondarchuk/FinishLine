import os

from project import app
from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Thread
from subprocess import Popen, PIPE


# запускает команду в shell и возвращает вывод
def run_cmd(cmd):
    process = Popen(cmd, stdout=PIPE, shell=True)
    return process.communicate()[0].decode('utf-8')


# удаляет контейнер и возвращает вывод команды
def force_remove_container(id):
    result = run_cmd(f'docker rm -f {id}')[:-1]
    print(f'Force removed: {result}')
    return result


# возвращает номер последней строки, содержащей подстроку line (-1 при отсутствии)
def find_last_line_in_logs(container, substr):
    result = run_cmd(f'''docker logs {container} 2>&1 | grep -n "{substr}" | tail --lines=1''')
    try:
        lineNumber = int(result[0:result.index(':')])
        return lineNumber
    except ValueError:
        return -1


# возвращает список айднишников запущенных контейнеров
def get_running_containers():
    result = run_cmd('docker ps -q --filter "ancestor=ride"')
    return result.splitlines()


# удаляет запущенные контейнеры, из которых вышел юзер (или все, если параметр True)
def clean_containers(cleanAll=False):
    for container in get_running_containers():
        clientEnter = find_last_line_in_logs(container, "Set client")
        clientExit = find_last_line_in_logs(container, "All contributions have been stopped")
        print(f'Container {container}: entered {clientEnter}, exited {clientExit}')
        if clientExit > clientEnter or cleanAll:
            force_remove_container(container)


INTERVAL_IN_SECONDS = 300
scheduler = BlockingScheduler()
scheduler.add_job(clean_containers, 'interval', seconds=INTERVAL_IN_SECONDS)
cleaner_thread = Thread(target=scheduler.start, args=())
cleaner_thread.start()

try:
    app.run(host='127.0.0.1', port='5000', debug=True)
finally:
    clean_containers(True)
    os._exit(0)
