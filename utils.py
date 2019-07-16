import json

from ssh import get_gpu_utils


def read_servers():
    with open("servers.json") as f:
        servers = json.load(f)
        print(servers)
        return servers


class ServerUtils:
    def __init__(self):
        self.servers = read_servers()

    def gpu_status(self):
        results = []
        for server in self.servers:
            try:
                if server["use"] is 1:
                    print("connect: " + server["server-name"])
                    gpu_infos, status = get_gpu_utils(server["hostname"], server["port"],
                                                      server["username"], server["password"])
                    results.append({"name": server["server-name"], "gpu_infos": gpu_infos, "status": status})
            except Exception as e:
                print(e)
                pass
        return results

        # if __name__ == "__main__":
        #     servers = read_servers()
        #     for server in servers:
        #         if server["use"] is 1:
        #             print("connect: " + server["server-name"])
        #             # get_server_status(server["hostname"], server["port"], server["username"], server["password"])
        #             print pretty_print(
        #                 get_gpu_utils(server["hostname"], server["port"],
        #                               server["username"], server["password"])
        #             )
