"""Builds index.html for GitHub Pages from the page source (the claude.ai artifact file) and adds the visit counter.

The counter only runs on the GitHub page (the claude.ai preview blocks requests to other sites anyway).
It sends no personal data: a random device id kept in the visitor's browser, the day, the page language
and whether it is a phone. Rules on the database only allow adding +1 to the totals.
"""
import os, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ['TEMP'], 'claude', 'D--webitoo-PythonApplication1',
                                                           '56eb3ed8-abd3-472c-b8a4-b1f5e0fe237f', 'scratchpad', 'webitoo-teacher-system.html')
DB = 'https://webitoo-control-default-rtdb.europe-west1.firebasedatabase.app'

COUNTER = """
<script>
// Visit counter (Webitoo): +1 visit every time the page opens, +1 device the first time a phone/PC opens it.
(function () {
  if (/[?&]nocount\\b/.test(location.search)) { try { localStorage.setItem('webitoo-nocount', '1'); } catch (e) {} }
  try { if (localStorage.getItem('webitoo-nocount') === '1') return; } catch (e) {}   // your own devices: open once with ?nocount
  var d = new Date(), day = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  var inc = { '.sv': { 'increment': 1 } }, base = 'prices/visits/', upd = {};
  upd[base + 'total_views'] = inc;
  upd[base + 'daily/' + day + '/views'] = inc;
  var id = null;
  try { id = localStorage.getItem('webitoo-device'); } catch (e) {}
  if (!id) {
    id = Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
    var saved = false;
    try { localStorage.setItem('webitoo-device', id); saved = true; } catch (e) {}
    if (saved) {
      upd[base + 'total_devices'] = inc;
      upd[base + 'daily/' + day + '/devices'] = inc;
      upd[base + 'devices/' + id] = { first: { '.sv': 'timestamp' }, mobile: /Mobi|Android|iPhone/i.test(navigator.userAgent),
                                       lang: (document.getElementById('page') || {}).lang || 'ar' };
    }
  }
  try { fetch('""" + DB + """/.json', { method: 'PATCH', body: JSON.stringify(upd), keepalive: true }).catch(function () {}); } catch (e) {}
})();
</script>
"""

src = open(SRC, encoding='utf-8').read()
head_end = src.index('</style>') + len('</style>')
head, body = src[:head_end], src[head_end:]
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
doc = ('<!doctype html>\n<html lang="ar">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       '<meta name="theme-color" content="#070b1a">\n'
       '<meta name="description" content="Webitoo Teacher System - attendance by barcode, automatic WhatsApp to parents, student portal. Prices and demo.">\n'
       + head + '\n<style>body{margin:0}</style>\n</head>\n<body>' + body + COUNTER + '\n</body>\n</html>\n')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'), 'w', encoding='utf-8').write(doc)
print('index.html', len(doc) // 1024, 'KB')
