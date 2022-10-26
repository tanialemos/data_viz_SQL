Select Code, Description
from code
where code.Category = "JuridicalSituation" AND code."Language"="FR";

CREATE TABLE TypeOfEnterprise AS
Select Code, Description
from code
where code.Category = "TypeOfEnterprise" AND code."Language"="FR";

CREATE TABLE TypeOfEnterprise AS
Select  Code, Description as b
from code
where code.Category = "JuridicalForm" AND code."Language"="FR";

CREATE TABLE Status 

Select  Code, Description
from code
where code.Category = 'Status' AND code."Language"="FR"


SELECT *
from code

