from iocbuilder import AutoSubstitution, Xml


class eurotherm3504(Xml):
        TemplateFile = "eurotherm3504.xml"


class eurotherm3504Archive(AutoSubstitution):
        TemplateFile = "eurotherm3504-archive.template"


class eurotherm3504Gui(AutoSubstitution):
        TemplateFile = "eurotherm3504-gui.template"


class eurotherm2k(Xml):
        TemplateFile = "eurotherm2k.xml"


class eurotherm2kArchive(AutoSubstitution):
        TemplateFile = "eurotherm2k-archive.template"


class eurotherm2kGui(AutoSubstitution):
        TemplateFile = "eurotherm2k-gui.template"

