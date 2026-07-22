import importDailyUses
import importMonthDefaultUsage
import importSimInventory

def importFiles():
    importDailyUses.importDailyUses()
    importMonthDefaultUsage.importMonthDefaultUsage()
    importSimInventory.importSimInventory()

if __name__ == "__main__":
    importFiles()