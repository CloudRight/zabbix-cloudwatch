#!/usr/bin/env python2
from basic_discovery import BasicDiscoverer


class Discoverer(BasicDiscoverer):
    def discovery(self, *args):

        response = self.client.list_metrics(Namespace="AWS/Lambda")

        data = []

        for Function in response["Metrics"]:
            for Dimension in Function["Dimensions"]:
                if Dimension["Name"] == "FunctionName":
                    # Discovery entry
                    ldd = {
                        "{#LAMBDA_FUNCTION_NAME}": Dimension["Value"],
                    }

                    if ldd not in data:
                        data.append(ldd)

        return data
