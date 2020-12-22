from .basic_discovery import BasicDiscoverer


class Discoverer(BasicDiscoverer):
    def discovery(self, *args):
        data = list()

        for cluster in self.client.list_clusters()["clusterArns"]:
            for service in self.client.list_services(cluster=cluster)["serviceArns"]:
                ldd = {
                    "{#CLUSTERNAME}": service.split("/")[-2],
                    "{#SERVICENAME}": service.split("/")[-1],
                }
                data.append(ldd)
        return data

