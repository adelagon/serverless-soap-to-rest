from spyne import Application, rpc, ServiceBase, Float, Integer, Unicode

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class InsuranceService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, Unicode, Integer, Float, _returns=Float)
    def submit_car_application(ctx, first_name, last_name, make, model, year, current_price):
        """Docstrings for service methods appear as documentation in the wsdl.
        <b>What fun!</b>
        @param first_name First Name of the owner
        @param last_name Last Name of the owner
        @param make Car Make
        @param mode Car Model
        @param year Car Year
        @param current_price Current Value of the Car
        @return insurance_value
        """
        return current_price * 0.10

application = Application([InsuranceService], 'spyne.insurance.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://0.0.0.0:8000")
    logging.info("wsdl is at: http://0.0.0.0:8000/?wsdl")

    server = make_server('0.0.0.0', 8000, wsgi_application)
    server.serve_forever()