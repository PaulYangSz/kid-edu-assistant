import sys
from os import path

import factory
import log

from gevent import pywsgi


def absdirpath(file, *parts):
    """Returns the absolute path to the file directory.

    Args:
      file: usually the __file__ attribute.
      parts: optional path parts to be concatenated.
    """
    return path.join(path.abspath(path.dirname(file)), *parts)


if __name__ == "__main__":
    host = '0.0.0.0'
    port = int(sys.argv[1]) if len(sys.argv) >= 2 else 11504
    app = factory.create_app(absdirpath(__file__, '.', 'config', 'assistant_server_test.cfg'))
    log.info('Starting server on: %s:%d.' % (host, port))
    server = pywsgi.WSGIServer((host, port), app)
    server.serve_forever()
    # app.run(debug=True, host='172.16.30.163', port=5001, threaded=True)
