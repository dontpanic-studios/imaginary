from src.support.library.ipl.host import Host

class ThemeInject:
    def Main():
        modules = Host.getModules()
        print(f"CustomPlugin: Modules\n{modules}")
        print("Sample Plugin Done.")