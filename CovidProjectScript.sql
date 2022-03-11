-- Total cases vs total deaths
-- Shows likelihood of dying if you contract covid in your country
select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as Death_Percentage
from coviddeath
where continent is not null
order by 1,2;

-- Total cases vs population
-- percentage of populatio got Covid
select location, date, population, total_cases, (total_cases/population)*100 as Cases_Percentage
from coviddeath
where continent is not null
order by 1,2;

-- Countries with highest infection rate compared to population
select location, population, max(total_cases) as HighestInfectionCount, max((total_cases/population))*100 as PercentPopulationInfected
from coviddeath
where continent is not null
group by location, population
order by PercentPopulationInfected desc;

-- highest death count per population by countries
select location, max(total_deaths) as TotalDeathCount
from coviddeath
where continent is not null
group by location
order by TotalDeathCount desc;

-- highest death count per population by continents
select continent, max(total_deaths) as TotalDeathCount
from coviddeath
where continent is not null
group by continent
order by TotalDeathCount desc;

-- Global Numbers
select year(date) as Year, month(date) as Month, sum(new_cases) as total_cases, sum(new_deaths) as total_deaths, 
sum(new_deaths)/sum(new_cases) * 100 as DeathPercentage
from coviddeath
where continent is not null
group by year(date), month(date)
order by 1;

-- Join coviddeath and covidVaccination tables
-- Shows percentage of population that has received at least one Covid Vaccine
-- CTE
With PopvsVac(Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated)
as
(
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
sum(vac.new_vaccinations) over (partition by dea.location Order by dea.location, 
dea.date) as RollingPeopleVaccinated
from coviddeath dea
join covidvaccination vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
)
select *, (RollingPeopleVaccinated/population)*100
from PopvsVac;

-- Use temp table to perform calculation on Partition By in previous query
Drop table if exists percentpopulationvaccinated;
Create Table PercentPopulationVaccinated
(
Continent varchar(100),
Location varchar(100),
Date datetime,
Population int,
New_vaccinations int,
RollingPeopleVaccinated double
);

Insert into PercentPopulationVaccinated
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
sum(vac.new_vaccinations) over (partition by dea.location Order by dea.location, 
dea.date) as RollingPeopleVaccinated
from coviddeath dea
join covidvaccination vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null;

select *, (RollingPeopleVaccinated/population)*100
from PercentPopulationVaccinated;

-- Create View for visualization
create view PopulationVaccinatedPercentage as
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
sum(vac.new_vaccinations) over (partition by dea.location Order by dea.location, 
dea.date) as RollingPeopleVaccinated
from coviddeath dea
join covidvaccination vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null;

-- For tableau visualization
-- 1.
select sum(new_cases) as total_cases, sum(new_deaths) as total_deaths, 
sum(new_deaths)/sum(new_cases) * 100 as DeathPercentage
from coviddeath
where continent is not null;

-- 2.
select location, sum(new_deaths) as TotalDeathCount 
from coviddeath
where continent is null
and location not REGEXP 'World|European Union|International|income'
group by location
order by TotalDeathCount desc;

-- 3.
select location, ifnull(population,0) as Population, ifnull(max(total_cases),0) as HighestInfectionCount, 
ifnull(max((total_cases/population))*100,0) as PercentPopulationInfected
from coviddeath
group by location, population
order by PercentPopulationInfected desc;

-- 4.
select 'Location', 'Population', 'Date', 'HighestInfectionCount', 'PercentPopulationInfected'
union all 
select location, ifnull(population,0) as population, date, ifnull(max(total_cases),0) as HighestInfectionCount, 
ifnull(max((total_cases/population))*100,0) as PercentPopulationInfected
from coviddeath
where continent is not null
group by location, population, date
order by location asc, date asc
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Tableau Table 4.csv' 
    FIELDS ENCLOSED BY '"' 
    TERMINATED BY ',' 
    ESCAPED BY '"' LINES
    TERMINATED BY '\r\n';
    
select location, ifnull(population,0) as population, date, ifnull(max(total_cases),0) as HighestInfectionCount, 
ifnull(max((total_cases/population))*100,0) as PercentPopulationInfected
from coviddeath
where continent is not null
and location like '%states%'
group by date
order by location asc, date asc



