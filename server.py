import asyncio

data_map = {}

async def put(list_to_read, writer):
    if len(list_to_read) > 3:
        raise ValueError

    key = list_to_read[0]
    timestamp = int(list_to_read[2])
    value = float(list_to_read[1])

    data_map[key] = data_map.get(key, dict())
    data_map[key][timestamp] = value

    writer.write("ok\n\n".encode())
    await writer.drain()


async def send_data(key, writer):
    send_string = "ok\n"
    if key in data_map:
        for timestamp in data_map[key]:
            send_string += f"{key} {data_map[key][timestamp]} {timestamp}\n"
        send_string += '\n'
    else:
        send_string += '\n'

    writer.write(send_string.encode())
    await writer.drain()


async def send_all_data(writer):
    send_string = "ok\n"
    for key in data_map:
        for timestamp in data_map[key]:
            send_string += f"{key} {data_map[key][timestamp]} {timestamp}\n"
    send_string += '\n'

    writer.write(send_string.encode())
    await writer.drain()


async def get(list_to_read, writer):
    # get palm.cpu\n
    # get *\n
    if len(list_to_read) > 1:
        raise TypeError

    if list_to_read[0] == '*':
        await send_all_data(writer)
    else:
        await send_data(list_to_read[0], writer)


async def get_command(message):
    #'put palm.cpu 23.7 1150864247\n'
    #'get palm.cpu\n'
    #'get *\n'
    list_to_read = message.split()
    command = list_to_read.pop(0)
    return (command, list_to_read)


async def execute_command(command, list_to_read, writer):
    if command == 'put':
        await put(list_to_read, writer)
    elif command == 'get':
        await get(list_to_read, writer)
    else:
        raise TypeError


async def handle_echo(reader, writer):
    while True:
        try:
            data = await reader.read(1024)
            if not data:
                break

            message = data.decode()

            command, list_to_read = await get_command(message)
            await execute_command(command, list_to_read, writer)
        except (IndexError, ValueError, KeyError, TypeError) as ex:
            writer.write("error\nwrong command\n\n".encode())
            await writer.drain()


    writer.close()


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, host, port, loop=loop)

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()