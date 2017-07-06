def build_connection_string(driver, host, port, db):
    return "jdbc:%s/%s:%s/%s" % (driver, host, port, db)