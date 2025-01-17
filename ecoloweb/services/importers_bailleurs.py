from datetime import date

from django.conf import settings

from bailleurs.models import Bailleur

from . import SiretResolver
from .importers import ModelImporter


class BailleurImporter(ModelImporter):
    model = Bailleur

    def __init__(self, departement: str, import_date: date, debug=False, update=False):
        super().__init__(departement, import_date, debug=debug, update=update)

        self._identity_keys = ["siren"]
        try:
            self._siret_resolver = SiretResolver(
                settings.INSEE_API_KEY, settings.INSEE_API_SECRET
            )
        except BaseException:
            self._siret_resolver = None

        self._query_one = self._get_file_content("importers/bailleur.sql")

    def _resolve_siret(self, codesiren: str, date_creation: date):

        if self._siret_resolver:
            try:
                return self._siret_resolver.resolve(codesiren, date_creation)
            except BaseException:
                return None

        return None

    def _prepare_data(self, data: dict) -> dict:
        codesiret = data.pop("codesiret")
        date_creation = data["cree_le"]

        data["siret"] = codesiret

        # Clean SIRET code
        if (
            data["nature_bailleur"] != "Bailleurs privés"
            and len(codesiret) != 14
            and (siret := self._resolve_siret(codesiret, date_creation)) is not None
        ):
            data["siret"] = siret

        return data
