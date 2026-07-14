import json, os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
import requests as req

app = Flask(__name__, static_folder='.')
ROOT     = Path(__file__).parent
MODS_FILE = ROOT.parent.parent / 'mods.json'
COH_DATA  = Path('/Applications/coh/data')
DOWNLOADS = ROOT / 'downloads'
DOWNLOADS.mkdir(exist_ok=True)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/core/<path:filename>')
def core(filename):
    return send_from_directory('../core', filename)


@app.route('/api/mods')
def api_mods():
    return jsonify(json.loads(MODS_FILE.read_text()))


@app.route('/api/installed')
def api_installed():
    target = COH_DATA if COH_DATA.exists() else DOWNLOADS
    return jsonify([f.stem for f in target.glob('*.pigg')])


@app.route('/api/install', methods=['POST'])
def api_install():
    data = request.get_json(silent=True) or {}
    mod_id   = data.get('id')
    url      = data.get('download_url')
    if not url:
        return jsonify({'ok': False, 'error': 'missing download_url'}), 400
    try:
        r = req.get(url, timeout=60, stream=True)
        r.raise_for_status()
        fname = url.split('file=')[-1].split('/')[-1] or f'mod-{mod_id}.pigg'
        dest  = (COH_DATA if COH_DATA.exists() else DOWNLOADS) / fname
        dest.write_bytes(r.content)
        return jsonify({'ok': True, 'path': str(dest), 'id': mod_id})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print('CoX Mod Server → http://localhost:7777')
    app.run(host='127.0.0.1', port=7777, debug=True)
