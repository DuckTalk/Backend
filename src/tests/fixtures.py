import pathlib
import os

import pytest
from xprocess import ProcessStarter, XProcess

@pytest.fixture
def server(xprocess: XProcess):
    class Starter(ProcessStarter):
        # startup pattern
        pattern = "Server started"

        # server dir
        env = os.environ.copy()
        env["PATH"] = str(pathlib.Path(__file__).parent.parent)

        # command to start process
        args = ["py", "src/app.py", "--dbfile", "src/tests/test.db", "-p", "2007"]

    # ensure process is running and return its logfile
    logfile = xprocess.ensure("myserver", Starter)

    conn = "http://ableytner.ddns.net:2007" # create a connection or url/port info to the server
    yield conn

    # clean up whole process tree afterwards
    xprocess.getinfo("myserver").terminate()
    if os.path.isfile("src/tests/test.db"):
        os.remove("src/tests/test.db")
