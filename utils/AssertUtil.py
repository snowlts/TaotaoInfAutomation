import json
import os

from .LogUtil import logger_init

logger = logger_init(os.path.basename(__file__))


class Assert:
    def assert_code(self,code,expected):
        try:
            assert code == expected
            return True
        except:
            logger.error("Error code: code is %s, code expected %s" % (code, expected))
            raise
    def assert_body(self,body,expected):
        if isinstance(expected,str):
            expected = json.loads(expected.encode('utf8'))
        try:
            assert body == expected
            return True
        except:
            logger.error("Error body: body is %s, body expected %s" % (body, expected))
            raise

    def assert_contains(self,body,expected):
        try:
            assert expected in json.dumps(body,sort_keys=False)
            return True
        except:
            logger.error("Error body: string %s not in body %s," % (expected,body))
            raise

    def assert_body_fields(self,body_fields,expected):
        logger.info("%s,body_fields:%s,expected: %s" % ('assert_body_fields',body_fields,expected) )
        for k,v in body_fields.items():
            exp = expected.get(k, None)
            if exp:
                try:
                    logger.info("assert field: %s, value: %s with expect value: %s" % (k,v,exp))
                    assert exp == v
                    return True
                except:
                    logger.error("Error field: field %s value %s,expected value %s" % (k,v,exp))
            else:
                logger.error("Error field: field %s not expected" % k)
                raise AssertionError("Error field: field %s not expected" % k)

