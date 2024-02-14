from PyQt6.QtWidgets import QApplication, QWidget, QPushButton,QFileDialog, QVBoxLayout, QLabel
from pandas import read_excel,ExcelFile

def read_excel_file(path):
    # skip first row
    df = ExcelFile(path)
    
    file = df.parse(df.sheet_names[0], skiprows=1)
    header_list = file.columns.tolist()
    print(file.columns) 
    # ['Student Id', 'Student Name', 'Gender', 'Program - Major', 'Category',
    #    'School Name', 'Department', 'CGPA', 'Nationality', 'Hostel', 'DC/ PB',
    #    'Club', 'Sports', 'Attendence', 'Email', 'Remarks']

    # print Gender column
    print(file['Gender'])

    return header_list, file
    

    # print(df.sheet_names)

    
def open_file():
    path = QFileDialog.getOpenFileName()
    if path[0]:
        read_excel_file(path[0])




def main():
    app = QApplication([])

    window = QWidget()
    window.setWindowTitle("Excel Reader")
    window.setGeometry(0, 0, 300, 300)
    layout = QVBoxLayout()
    button = QPushButton("Open file")
    button.clicked.connect(open_file)
    layout.addWidget(button)
    window.setLayout(layout)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()