import multiprocessing as mp
import socket, time
from classes import ROVManager


def start_server(server_ip, port_var):
    print('ROV should connect to {}'
          .format(socket.gethostbyname(socket.gethostname())))
    mgr = ROVManager(role='server', address=server_ip, port=port_var)


def control_main(server_ip, port_cam, port_var, camera_resolution, fullscreen):
    server = mp.Process(target=start_server, args=(server_ip, port_var))
    server.start()
    time.sleep(2)

    mgr = ROVManager(role='client', address='127.0.0.1', port=port_var)

    try:
        while mgr.system().get('shutdown') is False:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('User aborted operation')
    finally:
        print('Shutting down server')
        time.sleep(1)
        server.terminate()
