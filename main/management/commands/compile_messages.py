"""
Compile .po files to .mo without requiring GNU gettext (uses polib).
Run: python manage.py compile_messages
"""
from pathlib import Path
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Compile .po translation files to .mo (no GNU gettext required)'

    def handle(self, *args, **options):
        try:
            import polib
        except ImportError:
            self.stderr.write(self.style.ERROR('polib not installed. Run: pip install polib'))
            return

        locale_dir = Path(__file__).resolve().parents[3] / 'locale'
        if not locale_dir.exists():
            self.stderr.write(self.style.ERROR(f'locale/ directory not found'))
            return

        compiled = 0
        for po_path in locale_dir.rglob('*.po'):
            mo_path = po_path.with_suffix('.mo')
            po = polib.pofile(str(po_path), encoding='utf-8')
            po.save_as_mofile(str(mo_path))
            lang = po_path.parent.parent.name
            self.stdout.write(self.style.SUCCESS(
                f'  OK [{lang}] {len(po)} entries compiled'
            ))
            compiled += 1

        self.stdout.write(self.style.SUCCESS(f'Done: {compiled} file(s) compiled'))
