from flask import current_app as app, request as req, abort
from .strip import strip

def get_state():
    strip_state = list(col.hex for col in strip)
    colors = set(strip_state)
    uniformState = next(iter(colors)) if len(colors) == 1 else None
    return {
        'uniformState': uniformState,
        'stripState': strip_state
    }

@app.route('/state')
def show_state():
    return get_state()

@app.route('/state', methods=['POST'])
def update_state():
    jsn = req.get_json()
    print(jsn)
    if jsn:
        if 'state' not in req.json:
            abort(400, 'missing state parameter')
        if isinstance(jsn, dict):
            state = jsn['state']
        elif isinstance(jsn, (str, list)):
            state = jsn
        else:
            abort(400, 'invalid content')
    elif req.form:
        state = req.form['state']
    elif req.content_type == 'text/plain':
        state = str(req.data, encoding='utf8')
    else:
        abort(400, 'invalid content')
    
    with strip:
        strip.state = state
    return get_state()
