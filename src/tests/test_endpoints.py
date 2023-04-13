import requests

def test_exist(server):
    endpoints = [
        ("salt", (True, False, False)),
        ("token", (True, False, True)),
        ("message", (True, True, True)),
        ("user", (True, True, True)),
        ("group", (True, True, True))
    ]
    for ep, results in endpoints:
        res_get = requests.get(f"{server}/api/{ep}", json={}, timeout=1)
        res_post = requests.post(f"{server}/api/{ep}", json={}, timeout=1)
        res_del = requests.delete(f"{server}/api/{ep}", json={}, timeout=1)

        if results[0]:
            assert res_get
            assert res_get.status_code == requests.codes.OK
        if results[1]:
            assert res_post
            assert res_post.status_code == requests.codes.OK
        if results[2]:
            assert res_del
            assert res_del.status_code == requests.codes.OK
