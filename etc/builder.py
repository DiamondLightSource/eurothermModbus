from iocbuilder import AutoSubstitution
from iocbuilder import Device
from iocbuilder.modules.modbus import modbusPort
from iocbuilder.modules.modbus import modbusInterpose
from iocbuilder.modules.asyn import AsynIP
from iocbuilder.arginfo import *

MODBUS_PREFIX_INDEX = 1


class _EurothermDisable(AutoSubstitution):
    TemplateFile = "eurothermDis.template"


class _EurothermLoop(AutoSubstitution):
    TemplateFile = "eurothermLoop.template"

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

    def __init__(self, name, port, device, ipaddress, tcpport=502, rregu="C/s",
                 noAutoConnect=False):
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
        self.loop1 = _EurothermLoop(device=device,
                               modbus_prefix=self.modbus_prefix,
                               loop_name='LOOP1',
                               rregu=self.rregu_options.index(self.rregu),
                               autotune_addr=270,
                               derivative_addr=9,
                               integral_addr=8,
                               mode_addr=273,
                               output_addr=3,
                               outputhi_addr=30,
                               outputlo_addr=31,
                               proportional_addr=6,
                               temperature_addr=1,
                               ramprate_addr=35,
                               setpoint_addr=2,
                               working_setpoint_addr=5)
        self.__super.__init__()

    rregu_options = ["C/s", "C/min"]
    ArgInfo = makeArgInfo(__init__,
                          name=Simple("Eurotherm name", str),
                          port=Simple("Port name", str),
                          device=Simple("Device prefix used in PVs", str),
                          ipaddress=Simple("Eurotherm ip address", str),
                          tcpport=Simple("Tcp port", int),
                          noAutoConnect=Simple("Don't autoconnect", bool),
                          rregu=Choice("Ramprate EGU", rregu_options))

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
    linktype = "tcpip"

    def __init__(self, **kwargs):
        self.__super.__init__(**kwargs)
        self.loop2 = _EurothermLoop(device=self.device,
                               modbus_prefix=self.modbus_prefix,
                               loop_name='LOOP2',
                               rregu=self.rregu_options.index(self.rregu),
                               autotune_addr=1294,
                               derivative_addr=1033,
                               integral_addr=1032,
                               mode_addr=1297,
                               output_addr=1027,
                               outputhi_addr=1054,
                               outputlo_addr=1055,
                               proportional_addr=1030,
                               temperature_addr=1025,
                               ramprate_addr=1059,
                               setpoint_addr=1026,
                               working_setpoint_addr=1029)
        self.prog = _EurothermProg(device=self.device,
                                   modbus_prefix=self.modbus_prefix)
        self.rec = _EurothermRec(device=self.device,
                                 modbus_prefix=self.modbus_prefix)
        self.gui = _Eurotherm3kGui(name=self.name, device=self.device)
        self.arch = _Eurotherm3kArchive(device=self.device)

class Eurotherm3Krtu(_Eurotherm):
    linktype = "rtu"

    def __init__(self, **kwargs):
        self.__super.__init__(**kwargs)
        self.loop2 = _EurothermLoop(device=self.device,
                               modbus_prefix=self.modbus_prefix,
                               loop_name='LOOP2',
                               rregu=self.rregu_options.index(self.rregu),
                               autotune_addr=1294,
                               derivative_addr=1033,
                               integral_addr=1032,
                               mode_addr=1297,
                               output_addr=1027,
                               outputhi_addr=1054,
                               outputlo_addr=1055,
                               proportional_addr=1030,
                               temperature_addr=1025,
                               ramprate_addr=1059,
                               setpoint_addr=1026,
                               working_setpoint_addr=1029)
        self.prog = _EurothermProg(device=self.device,
                                   modbus_prefix=self.modbus_prefix)
        self.rec = _EurothermRec(device=self.device,
                                 modbus_prefix=self.modbus_prefix)
        self.gui = _Eurotherm3kGui(name=self.name, device=self.device)
        self.arch = _Eurotherm3kArchive(device=self.device)
