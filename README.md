# Data_viz_SQL
Descriptive analysis of a market


Tables
- Establishment : 1 ligne par unité d’établissement avec quelques données d’identification de base
    - EstablishmentNumber: Le numéro de l’unité d’établissement. 9.999.999.999
    - StartDate: La date de début de l’unité d’établissement.
    - EnterpriseNumber: Le numéro d’entreprise de l’entité enregistrée à laquelle appartient cette unité d’établissement. 9999.999.999

- entreprise :  1 ligne par entité enregistrée avec quelques données d’identification de base
    - EnterpriseNumber: Le numéro d’entreprise. 9999.999.999
    - Status: Le statut de l’entité enregistrée. Dans ce fichier, le format est toujours ‘AC’ : actif.
    - JuridicalSituation: La situation juridique de l’entité enregistrée. Voir table des codes.
    - TypeOfEnterprise: Le type d’entité enregistrée : entité enregistrée personne morale1 ou personne physique. Voir table des codes.
    - JuridicalForm: La forme légale de l’entité enregistrée, s’il s’agit d’une entité enregistrée personne morale. Voir table des codes.
    - StartDate: La date de début de l’entité enregistrée

- DENOMINATION : Une entité enregistrée, une unité d’établissement ou une succursale peut avoir différentes dénominations
    - EntityNumber: Le numéro d’unité d’établissement ou d’entreprise. 9999.999.999 ou
9.999.999.999
    - Language: Langue de la dénomination. Voir table des codes.
    - TypeOfDenomination: Type de dénomination. Voir table des codes.
    - Denomination: La dénomination de l’entreprise, de la succursale ou de l’unité d’établissement.

- CONTACT : 1 ligne par donnée de contact d’une entité enregistrée ou d’une unité d’établissement. Plusieurs données de contact peuvent être mentionnées pour une entité enregistrée ou unité d’établissement
    - EntityNumber: Le numéro d’unité d’établissement ou d’entreprise. 9999.999.999 of 9.999.999.999
    - EntityContact: Indique à quel type d’entité se rapporte la donnée de contact : entité, succursale ou unité d’établissement. Voir table des codes.
    - ContactType: Indique le type de donnée de contact : numéro de téléphone, e-mail ou adresse
internet. Voir table des codes.
    - Value: La donnée de contact c-à-d un numéro de téléphone, un e-mail ou une adresse
internet

