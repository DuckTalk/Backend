import psutil
import os

if __name__ == "__main__":
    pid_file = ".pytest_cache/d/.xprocess/myserver/xprocess.PID"

    if not os.path.isfile(pid_file):
        print("server not running!")
    else:
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())

        for p in psutil.process_iter():
            if p.pid == pid:
                p.terminate()
                p.wait()
                print("terminated")
        os.remove(pid_file)
