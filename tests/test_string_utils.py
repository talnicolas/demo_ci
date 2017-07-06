from app.string_utils import build_connection_string

def test_build_connection_string():
    driver = 'mysql'
    host = 'localhost'
    port = 3306
    db = 'demo'

    res = build_connection_string(driver, host, port, db)

    assert res == "jdbc:mysql//localhost:3306/demo"