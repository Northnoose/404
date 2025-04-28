
import polib
import os

def compile_po_to_mo(po_path):
    mo_path = po_path.replace('.po', '.mo')
    po = polib.pofile(po_path)
    po.save_as_mofile(mo_path)
    print(f"Kompilerte: {mo_path}")

    
if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    po_files = [
        os.path.join(base_dir, 'locale', 'en', 'LC_MESSAGES', 'django.po'),
        os.path.join(base_dir, 'locale', 'nb', 'LC_MESSAGES', 'django.po'),
    ]

    for po_file in po_files:
        if os.path.exists(po_file):
            compile_po_to_mo(po_file)
        else:
            print("Fant ikke:", po_file)

