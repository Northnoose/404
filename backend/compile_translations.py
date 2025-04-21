import polib
import os

def compile_mo_file(po_path):
    po = polib.pofile(po_path)
    mo_path = po_path.replace('.po', '.mo')
    po.save_as_mofile(mo_path)
    print(f"✅ Kompilert: {mo_path}")

base_dir = os.path.dirname(__file__)
po_file = os.path.join(base_dir, 'api', 'locale', 'en', 'LC_MESSAGES', 'django.po')
compile_mo_file(po_file)
