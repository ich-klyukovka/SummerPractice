import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Genetic Algorithm Solver")
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# 24 57 93 15 68 42 79 36 51 88 11 65 30 84 19 47 22 73 95 3 56 28 44 77 91 6 38 60 12 99 82 17 53 40 85 70 26 49 8 64 35 90 2 59 31 74 97 20 45 10 67 14 78 33 92 25 61 7 86 41 50 98 5 71 23 39 16 81 54 27 9 62 37 94 48 13 72 29 63 80 43 21 58 4 75 87 32 66 18 52 34 96 69 55 1 83 46 89 76 100  