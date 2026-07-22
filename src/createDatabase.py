import createAllRawMonthDefaultUsage
import createDailyUsage
import createImportedFileHash
import createRollingLastUsage
import createSimsInventory


def createDatabase():
    createAllRawMonthDefaultUsage.createAllRawMonthDefaultUsage()
    createDailyUsage.createDailyUsageDatabase()
    createImportedFileHash.createImportedFileHash()
    createRollingLastUsage.createRollingLastUsage()
    createSimsInventory.createSimsInventory()

if __name__ == "__main__":
    createDatabase()