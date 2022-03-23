import socket
import sys
import pickle

if __name__ == '__main__':
    # check if three arguments are entered or not
    if len(sys.argv) != 3:
        print("Usage: python client.py HOST PORT")
        exit(1)

    # set host and port
    host = sys.argv[1]
    port = int(sys.argv[2])

    # get access for a communication port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # check if connection is successful
        try:
            s.connect((host, port))
        except socket.error as error:
            print("failed to connect: {" + str(error) + "}")
            exit(1)
        # send pickled "JOIN" to request for access
        s.sendall(pickle.dumps('JOIN'))
        # receive returned member
        data = s.recv(1024)
        # unpickle member
        members = pickle.loads(data)
        print(f"JOIN ('{host}', {port})")

        # connect to three group members
        for value in members:
            # get access for a communication port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as x:
                # check if connection is successful
                try:
                    x.connect((value["host"], value["port"]))
                    print("Hello to {'host': '" + (value["host"] + "', 'port': " + str(value["port"])) + "}")
                except socket.error as error:
                    print("failed to connect: {}" + str(error))
                    continue

                # send pickled "HELLO" to request for access
                x.sendall(pickle.dumps('HELLO'))
                # receive returned message
                data = x.recv(1024)
                # unpickle message
                msg = pickle.loads(data)
                print(repr(msg))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
