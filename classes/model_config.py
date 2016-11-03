import os
import json
import os
import re


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={} dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

VCAP_SERVICES = os.getenv('VCAP_SERVICES')
if VCAP_SERVICES is not None:
    dsn=get_elephantsql_dsn(VCAP_SERVICES)
else:
    dsn = """user='postgres' password='b_e_BTFVmUQvEpr-arXGfL25XHdaVrCX' host='jumbo.db.elephantsql.com' port=5432 dbname='dxxbzlpn'"""