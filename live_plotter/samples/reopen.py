from live_plotter.proxy.Server import Server

from live_plotter.proxy.ProxyFigure import ProxyFigure

with ProxyFigure():
    pass
Server().join()
with ProxyFigure():
    pass
