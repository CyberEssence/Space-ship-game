import cx_Freeze

executables = [cx_Freeze.Executable("game.py")]

cx_Freeze.setup(
    name="Space ships",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["ship.jpg"]}},
    executables = executables

    )