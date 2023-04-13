from threading import Thread
from time import sleep

import pytest

@pytest.fixture
def server():
    import app
    Thread(target=app.run_app, args=(["--dbfile", "src/tests/test.db", "-p", "2007"],), daemon=True).start()
    sleep(1)
    yield "http://ableytner.ddns.net:2007"
