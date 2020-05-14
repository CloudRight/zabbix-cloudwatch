#!/usr/bin/env python2
from basic_discovery import BasicDiscoverer

import re

class Discoverer(BasicDiscoverer):
    def discovery(self, *args):

        response = self.client.list_functions()

        data = []

        for Function in response["Functions"]:

            # Discovery entry
            ldd = {
                "{#LAMBDA_FUNCTION_NAME}": Function["FunctionName"],
            }

            data.append(ldd)

        return data
