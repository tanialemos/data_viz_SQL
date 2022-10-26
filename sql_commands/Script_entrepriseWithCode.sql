Select establishment.EstablishmentNumber
,	establishment.StartDate as Est_StartDate
,	establishment.EnterpriseNumber
,	Status as Ent_Status
,	JuridicalSituation.Description as JuridicalSituation
,	enterprise.StartDate as Ent_StartDate
,	TypeOfEnterprise.Description as TypeOfEnterprise
,	JuridicalForm.Description as JuridicalForm
from establishment
LEFT JOIN enterprise
ON establishment.EnterpriseNumber=enterprise.EnterpriseNumber
LEFT JOIN (Select code, Description
from code
where code.Category = "TypeOfEnterprise" AND code."Language"="FR") as TypeOfEnterprise
ON enterprise.TypeOfEnterprise=TypeOfEnterprise.code
LEFT JOIN (Select code, Description
from code
where code.Category = "JuridicalForm" AND code."Language"="FR") as JuridicalForm
ON enterprise.JuridicalForm=JuridicalForm.code
LEFT JOIN (Select code, Description
from code
where code.Category = "JuridicalSituation" AND code."Language"="FR") as JuridicalSituation
ON enterprise.JuridicalSituation=JuridicalSituation.code
--GROUP BY EstablishmentNumber