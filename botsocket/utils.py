from .settings import CHUNK_SIZE


def send_by_chunks(connection, data):
    # first = data[:chunk_size]
    # rest = data[chunk_size:]
    # first = data[:chunk_size]
    # rest = data[chunk_size:]
    # while first:
    #     connection.send(first)
    #     first = rest[:chunk_size]
    #     rest = rest[chunk_size:]
    first, rest = data[:CHUNK_SIZE], data[CHUNK_SIZE:]
    connection.send(first)
    if rest:
        send_by_chunks(connection, rest)


def recv_by_chunks(connection):
    # total = b''
    # data_chunk = ssl_sock.recv(chunk_size)
    # while data_chunk:
    #     total += data_chunk
    #     data_chunk = ssl_sock.recv(chunk_size)
    # return total
    data_chunk = connection.recv(CHUNK_SIZE)
    if len(data_chunk) == CHUNK_SIZE:
        return data_chunk + recv_by_chunks(connection)
    return data_chunk
