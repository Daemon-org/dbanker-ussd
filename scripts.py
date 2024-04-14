import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbanker.settings")
django.setup()

from base.utils import MomoTransaction

transaction = MomoTransaction()

print(transaction.add_charges(2000))