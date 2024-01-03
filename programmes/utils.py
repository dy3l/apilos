from collections import defaultdict

from programmes.models import Programme


def diff_programme_duplication(numero_operation: str) -> dict[str, list]:
    diff = defaultdict(list)

    for prog in Programme.objects.filter(
        parent__isnull=False, numero_galion=numero_operation
    ).all():
        for f in [
            "administration_id",
            "bailleur_id",
            # "adresse",
            # "code_postal",
            # "ville",
        ]:
            diff[f].append(getattr(prog, f, None))

    return {k: list(set(v)) for k, v in diff.items() if len(set(v)) > 1}
