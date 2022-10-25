-- Requête pour alimenter la table programmes_lot

-- Champs restants à mapper:
-- annexe_ateliers boolean not null
-- annexe_balcons boolean not null
-- annexe_celliers              boolean                  not null,
-- annexe_combles               boolean                  not null,
-- annexe_loggias               boolean                  not null,
-- annexe_resserres             boolean                  not null,
-- annexe_sechoirs              boolean                  not null,
-- annexe_soussols              boolean                  not null,
-- edd_classique                text,
-- edd_volumetrique             text,
-- lgts_mixite_sociale_negocies integer                  not null,
-- parent_id   FK(programmes_lot) dans le cas d'un avenant seulement ?

select
    md5(cdg.id||'-'||ff.code) as id, -- Les lots d'un programme sont tous les logements partageant le même financement
    cdg.id as programme_id,
    pl.bailleurproprietaire_id as bailleur_id,
    coalesce(pl.financementdate, now()) as cree_le,
    coalesce(pl.financementdate, now()) as mis_a_jour_le,
    ff.code as financement,
    pl.logementsnombretotal as nb_logements,
    case
        when coalesce(pl.logementsnombreindtotal, 0) > 0 and coalesce(pl.logementsnombrecoltotal, 0) > 0 then 'MIXTE'
        when coalesce(pl.logementsnombreindtotal, 0) > 0 then 'INDIVIDUEL'
        else 'COLLECTIF'
    end as type_habitat,
    ap1.id is not null as annexe_caves,
    ap2.id is not null as annexe_terrasses,
    ap3.id is not null as annexe_remises,
    case
        when pl.estderogationloyer and coalesce(pl.logementsnombreindtotal, 0) > 0 then pl.montantplafondloyerindinitial
        when pl.estderogationloyer and coalesce(pl.logementsnombrecoltotal, 0) > 0 then pl.montantplafondloyercolinitial
    end as loyer_derogatoire
from ecolo.ecolo_programmelogement pl
    inner join ecolo.ecolo_conventiondonneesgenerales cdg on pl.conventiondonneesgenerales_id = cdg.id and cdg.avenant_id is null
    inner join ecolo.ecolo_conventionapl c on cdg.conventionapl_id = c.id
    -- Financement
    inner join ecolo.ecolo_typefinancement tf on pl.typefinancement_id = tf.id
    inner join ecolo.ecolo_famillefinancement ff on tf.famillefinancement_id = ff.id
    -- Annexes
    left join ecolo.ecolo_annexe a1 on a1.programmelogement_id = pl.id
    left join ecolo.ecolo_valeurparamstatic ap1 on a1.typeannexe_id = ap1.id and ap1.subtype = 'TAN' and ap1.code = '7' -- Cave
    left join ecolo.ecolo_annexe a2 on a2.programmelogement_id = pl.id
    left join ecolo.ecolo_valeurparamstatic ap2 on a2.typeannexe_id = ap2.id and ap2.subtype = 'TAN' and ap2.code = '5' -- Terrasse
    left join ecolo.ecolo_annexe a3 on a3.programmelogement_id = pl.id
    left join ecolo.ecolo_valeurparamstatic ap3 on a3.typeannexe_id = ap3.id and ap3.subtype = 'TAN' and ap3.code = '8' -- Box
    {% if pk %}
where
    md5(cdg.id||'-'||ff.code) = '{{ pk }}'
    {% endif %}
order by cdg.id, ff.code