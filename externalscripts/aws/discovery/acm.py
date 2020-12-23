from .basic_discovery import BasicDiscoverer


class Discoverer(BasicDiscoverer):
    def discovery(self, *args):
        response = self.client.list_certificates()

        data = list()
        for certificate in response["CertificateSummaryList"]:
            certificate_data = {
                "{#ARN}": certificate["CertificateArn"],
                "{#DOMAIN}": certificate["DomainName"],
            }
            data.append(certificate_data)

        return data
