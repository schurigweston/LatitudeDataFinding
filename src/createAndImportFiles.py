import createDatabase
import importFiles

def createAndImportFile():
    createDatabase.createDatabase()
    importFiles.importFiles()

if __name__ == "__main__":
    createAndImportFile()