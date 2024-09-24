from cx_Freeze import *
import sys
includefiles=['icon.ico','bg.jpg','logo.png','password.png','st.png','student.png','user.png','main.py']
base=None
if sys.platform=="win32":
    base="Win32GUI"

shortcut_table=[
    ("DesktopShortcut",
     "DesktopFolder",
     "Student Management System",
     "TARGETDIR",
     "[TARGETDIR]\login.exe",
     None,
     None,
     None,
     None,
     None,
     None,
     "TARGETDIR",
     )
]
msi_data={"Shortcut":shortcut_table}

bdist_msi_options={'data':msi_data}
setup(
    version="0.1",
    description="Student Management System",
    author="Tanish Arya",
    name="Student Management System",
    options={'build_exe':{'include_files':includefiles},'bdist_msi':bdist_msi_options,},
    executables=[
        Executable(
            script="login.py",
            base=base,
            icon='icon.ico',
        )
    ]
)
