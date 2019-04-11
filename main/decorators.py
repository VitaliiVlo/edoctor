import json
from functools import wraps

from main.http import json_error


def parse_json(view_func):
    """Decorator which parse json from request.body to request.json"""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            if request.body:
                try:
                    request.json = json.loads(request.body.decode())
                except ValueError:
                    return json_error('Invalid JSON input')
            else:
                request.json = {}
        return view_func(request, *args, **kwargs)

    return _wrapped_view
