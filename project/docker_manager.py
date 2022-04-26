from subprocess import Popen, PIPE


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
    return (host, port, container)


# удаляет контейнер и возвращает вывод команды
def force_remove_container(id):
    result = run_cmd(f'docker rm -f {id}')[:-1]
    print(f'Force removed: {result}')
    return result


