from iocbuilder import AutoSubstitution
from iocbuilder import Device
from iocbuilder.modules.modbus import modbusPort
from iocbuilder.modules.modbus import modbusInterpose
from iocbuilder.modules.asyn import AsynIP
from iocbuilder.arginfo import *

MODBUS_PREFIX_INDEX = 1


class _EurothermDisable(AutoSubstitution):
    TemplateFile = "eurothermDis.template"


class _EurothermL1(AutoSubstitution):
    TemplateFile = "eurothermL1.template"


class _EurothermL2(AutoSubstitution):
    TemplateFile = "eurothermL2.template"


class _EurothermProg(AutoSubstitution):
    TemplateFile = "eurothermProg.template"


class _EurothermRec(AutoSubstitution):
    TemplateFile = "eurothermRec.template"


class _Eurotherm2kGui(AutoSubstitution):
    TemplateFile = "eurotherm2k-gui.template"


class _Eurotherm3kGui(AutoSubstitution):
    TemplateFile = "eurotherm3k-gui.template"


class _Eurotherm2kArchive(AutoSubstitution):
    TemplateFile = "eurotherm2k-archive.template"


class _Eurotherm3kArchive(AutoSubstitution):
    TemplateFile = "eurotherm3k-archive.template"


class _Eurotherm(Device):
    linktype = "tcpip"

    def __init__(self, name, port, device, ipaddress, tcpport=502, rregu="C/s", noAutoConnect=False):
        self.__dict__.update(locals())
        global MODBUS_PREFIX_INDEX
        self.modbus_prefix = "EURTHM_MB_{}".format(MODBUS_PREFIX_INDEX)
        MODBUS_PREFIX_INDEX += 1
        dest_address = "{}:{}".format(ipaddress, tcpport)
        rx_portname = "{}_MASTER_RX".format(self.modbus_prefix)
        tx_portname = "{}_MASTER_TX".format(self.modbus_prefix)

        self.ip = AsynIP(name=port, port=dest_address,
                         noProcessEos=True, noAutoConnect=noAutoConnect)
        self.modbus_interpose = modbusInterpose(portname=port,
                                                linktype=self.linktype,
                                                timeoutmsec=2000,
                                                writedelaymsec=0)
        self.rx_modbus = modbusPort(portname=rx_portname, tcpportname=port,
                                 slaveaddr=1, modbusfunction=3,
                                 modbusstartaddr=-1, modbuslen=1,
                                 datatype="UINT16",
                                 pollmsec=1000,
                                 plctype="")
        self.tx_modbus = modbusPort(portname=tx_portname, tcpportname=port,
                                 slaveaddr=1, modbusfunction=6,
                                 modbusstartaddr=-1, modbuslen=1,
                                 datatype="UINT16",
                                 pollmsec=0,
                                 plctype="")

        self.disable = _EurothermDisable(device=device)
        self.l1 = _EurothermL1(device=device, modbus_prefix=self.modbus_prefix,
                               rregu=rregu)
        self.__super.__init__()

    ArgInfo = makeArgInfo(__init__,
                          name=Simple("Eurotherm name", str),
                          port=Simple("Port name", str),
                          device=Simple("Device prefix used in PVs", str),
                          ipaddress=Simple("Eurotherm ip address", str),
                          tcpport=Simple("Tcp port", int),
                          rregu=Simple("Ramp Rate units", str),
                          noAutoConnect=Simple("Don't autoconnect", bool))

    def Initialise(self):
        print('asynSetOption("{port}", 0, "disconnectOnReadTimeout", "Y")'.\
            format(port=self.port))


class Eurotherm2K(_Eurotherm):
    linktype = "rtu"

    def __init__(self, **kwargs):
        self.__super.__init__(**kwargs)
        self.gui = _Eurotherm2kGui(name=self.name, device=self.device)
        self.arch = _Eurotherm2kArchive(device=self.device)


class Eurotherm3K(_Eurotherm):
    linktype = "tcpip" #FYI

    def __init__(self, **kwargs):
        self.__super.__init__(**kwargs)
        self.l2 = _EurothermL2(device=self.device,
                               modbus_prefix=self.modbus_prefix,
                               rregu=self.rregu)
        self.prog = _EurothermProg(device=self.device,
                                   modbus_prefix=self.modbus_prefix)
        self.rec = _EurothermRec(device=self.device,
                                 modbus_prefix=self.modbus_prefix)
        self.gui = _Eurotherm3kGui(name=self.name, device=self.device)
        self.arch = _Eurotherm3kArchive(device=self.device)
