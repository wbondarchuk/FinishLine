from subprocess import Popen, PIPE
from .models import Conteiners
from . import db


# запускает команду в shell и возвращает вывод
def run_cmd(cmd):
    process = Popen(cmd, stdout=PIPE, shell=True)
    return process.communicate()[0].decode('utf-8')


# запускает контейнер RIDE на случайном порту и возвращает кортеж (ip, port)
def run_container():
    host = '127.0.0.1'
    container = run_cmd(f'docker run --ip={host} --detach --publish 3000 ride')[:-1]
    port = int(run_cmd(
        "docker inspect -f '{{ (index (index .NetworkSettings.Ports \"3000/tcp\") 0).HostPort }}' " + container))
    print(f'Started RIDE container (id={container}) on ({host},{port})')
    container = container[:12]
    print(container)
    return host, port, container


# удаляет контейнер и возвращает вывод команды
def force_remove_container(id):
    print('c===================3')
    result = run_cmd(f'docker rm -f {id}')[:-1]
    Conteiners.query.filter_by(id=id).delete()
    db.session.commit()
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


def get_URL(id):
    pass