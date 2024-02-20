import csv
from queue import Queue

class Request:
    def __init__(self, arrival_time, request_file, process_duration):
        self.arrival_time = int(arrival_time)
        self.request_file = request_file
        self.process_duration = int(process_duration)

class Server:
    def __init__(self):
        self.current_request = None
        self.time_remaining = 0

    def tick(self):
        if self.current_request:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_request = None
    
    def busy(self):
        return self.current_request is not None
    
    def start_next(self, next_request):
        self.current_request = next_request
        self.time_remaining = next_request.process_duration

def simulateOneServer(filename):
    server = Server()
    request_queue = Queue()
    waiting_times = []

    with open(filename) as f:
        for row in csv.reader(f):
            request_time, file_name, process_time = row
            request_queue.put(Request(request_time, file_name, process_time))

    current_second = 0
    while not request_queue.empty() or server.busy():
        if not request_queue.empty():
            next_request = request_queue.queue[0]
            if next_request.arrival_time <= current_time:
                request_queue.get()
                if not server.busy():
                    waiting_times.append(current_time - next_request.arrival_time)
                    server.start_next(next_request)

        server.tick()
        current_time += 1

    average_wait = sum(waiting_times) / len(waiting_times) if waiting_times else 0
    print(f"Average Wait time with one server: {average_wait:.2f} seconds.")
    return average_wait

def simulateManyServers(filename, num_servers):
    servers = [Server() for _ in range(num_servers)]
    request_queue = Queue()
    waiting_times = []

    with open(filename) as f:
        for row in csv.reader(f):
            request_time, file_name, process_time = row
            request_queue.put(Request(request_time, file_name, process_time))

    current_time = 0
    server_index = 0
    while not request_queue.empty() or any(server.busy() for server in servers):
        if not request_queue.empty():
            next_request = request_queue.queue[0]
            if next_request.arrival_time <= current_time:
                request_queue.get()
                if not servers[server_index].busy():
                    waiting_times.append(current_time - next_request.arrival_time)
                    servers[server_index].start_next(next_request)
                    server_index = (server_index + 1) % num_servers

        for server in servers:
            server.tick()
        current_time += 1

    average_wait = sum(waiting_times) / len(waiting_times) if waiting_times else 0
    print(f"Average wait time with {num_servers} servers: {average_wait:.2f} seconds.")
    return average_wait

def main(filename, servers=1):
    if servers == 1:
        simulateOneServer(filename)
    else:
        simulateManyServers(filename, servers)

if __name__ == "__main__":
    main("C:/Users/Jessie/Documents/IS 211/requests.csv", servers=2)