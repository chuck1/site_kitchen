import sys

import oodb

def main():    
        app = oodb.gui.spreadsheet.Application(sys.argv)
        w = oodb.gui.spreadsheet.Window()
        sys.exit(app.exec_())

if __name__ == '__main__':
        main()
