from flask import Flask, request, jsonify
from pycomm3 import LogixDriver

types = {'INT': int,
         'SINT': int,
         'DINT': int,
         'REAL': float,
         'STRING': str,
         'String40': str,
         'BOOL': bool}

app = Flask(__name__)

plc_connections = dict()

@app.route('/', methods=['GET'])
def read():
    try:
        plc_path = request.args.get('plc')
        tag = request.args.get('tag')
        if plc_path in plc_connections.keys():
            plc = plc_connections[plc_path]
        else:
            plc = LogixDriver(plc_path)
            plc_connections[plc_path] = plc
        val = plc.read(tag).value
        return jsonify({'status': 'success', 'val': val})
    except:
        import traceback
        return jsonify({'status': 'error', 'val': traceback.format_exc()})

@app.route('/', methods=['PUT'])
def write():
    #try:
    plc_path = request.args.get('plc')
    if plc_path in plc_connections.keys():
        plc = plc_connections[plc_path]
    else:
        plc = LogixDriver(plc_path)
        plc_connections[plc_path] = plc
    tag = request.args.get('tag')
    tag_type = plc.tags[tag.split('[')[0]]['data_type_name']
    value = types[tag_type](request.args.get('value'))
    error = plc.write((tag, value)).error
    if error is not None:
        import traceback
        raise Exception(traceback.format_exc())
    return jsonify({'status': 'success'})

@app.route('/array/', methods=['PUT'])
def array_write():

    plc_path = request.args.get('plc')
    if plc_path in plc_connections.keys():
        plc = plc_connections[plc_path]
    else:
        plc = LogixDriver(plc_path)
        plc_connections[plc_path] = plc
    tag = request.args.get('tag')
    tag_type = plc.tags[tag.split('[')[0]]['data_type_name']
    value = types[tag_type](request.args.get('value'))
    error = plc.write((tag, value)).error
    if error is not None:
        import traceback
        raise Exception(traceback.format_exc())
    return jsonify({'status': 'success'})

@app.route('/array/', methods=['GET'])
def array_read():
    plc_path = request.args.get('plc')
    data = json.loads(request.data)
    if plc_path in plc_connections.keys():
        plc = plc_connections[plc_path]
    else:
        plc = LogixDriver(plc_path)
        plc_connections[plc_path] = plc
    tag = request.args.get('tag')
    tag_type = plc.tags[tag.split('[')[0]]['data_type_name']
    value = types[tag_type](request.args.get('value'))
    error = plc.write((tag, value)).error
    if error is not None:
        import traceback
        raise Exception(traceback.format_exc())
    return jsonify({'status': 'success'})

app.run(debug=True)