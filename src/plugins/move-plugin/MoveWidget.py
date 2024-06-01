from src.support.library.ipl.host import Host
from main import Main

class WidgetMovement:
    def Main():
        print(f"CustomPlugin: moving to 2, 4")
        print(f"modules: {Host.getWidgets()}")
        modules = Host.replaceWidget(Main.getWidget(), x=2, y=4)
        print("Sample Plugin Done.")