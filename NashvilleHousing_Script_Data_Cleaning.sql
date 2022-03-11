-- Load Nashville Housing dataset

LOAD DATA INFILE '.../Nashville_Housing.csv' INTO TABLE nashvillehousing
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- View the dataset
SELECT 
    *
FROM
    nashvillehousing;

-- update nashvillehousing set OWNERNAME = NULL where OWNERNAME = '';
  
/* CLEANING DATA */

-- STANDARDIZE DATE
ALTER TABLE nashvillehousing MODIFY saledate DATE;

-- POPULATE NULL PROPERTY ADDRESS

SELECT 
    *
FROM
    nashvillehousing
WHERE
    PropertyAddress IS NULL
ORDER BY ParcelID;

-- Looks like same Parcelid has the same property address
SELECT 
    parcelid, PropertyAddress, COUNT(parcelid)
FROM
    nashvillehousing
GROUP BY parcelid , PropertyAddress
HAVING COUNT(parcelid) > 1
;

-- Replace NULL property address based on the same ParcelID

SELECT 
    A.ParcelID,
    A.PropertyAddress,
    B.ParcelID,
    B.PropertyAddress,
    IFNULL(A.propertyaddress, B.propertyaddress)
FROM
    nashvillehousing A
        JOIN
    nashvillehousing B ON A.ParcelID = B.ParcelID
        AND A.UniqueID <> B.UniqueID
WHERE
    A.propertyaddress IS NULL;

UPDATE nashvillehousing A
        INNER JOIN
    nashvillehousing B ON A.ParcelID = B.ParcelID
        AND A.uniqueID <> B.UniqueID 
SET 
    A.PropertyAddress = IFNULL(A.propertyaddress, B.propertyaddress)
WHERE
    A.propertyaddress IS NULL;

-- SPLIT PROPERTY AND OWNER ADDRESS INTO ADDRESS, CITY AND STATE COLUMNS

SELECT 
    propertyaddress,
    SUBSTRING_INDEX(propertyaddress, ',', 1) AS Property_Address,
    SUBSTRING_INDEX(propertyaddress, ',', - 1) AS Property_City
FROM
    nashvillehousing;
    
SELECT 
    OwnerAddress,
    SUBSTRING_INDEX(Owneraddress, ',', 1) AS Owner_Address,
    SUBSTRING_INDEX(SUBSTRING_INDEX(Owneraddress, ',', 2),',',-1) AS Owner_City,
    SUBSTRING_INDEX(Owneraddress, ',', - 1) AS Owner_State
FROM
    nashvillehousing;

ALTER TABLE nashvillehousing
ADD Property_Address varchar(100),
ADD Property_City varchar(100),
ADD Owner_Address varchar(100),
ADD Owner_City varchar(100),
ADD Owner_State varchar(100)
;

UPDATE nashvillehousing 
SET 
    Property_Address = SUBSTRING_INDEX(propertyaddress, ',', 1),
    Property_City = SUBSTRING_INDEX(propertyaddress, ',', -1),
    Owner_Address = SUBSTRING_INDEX(Owneraddress, ',', 1),
    Owner_City = SUBSTRING_INDEX(SUBSTRING_INDEX(Owneraddress, ',', 2), ',', -1),
    Owner_State = SUBSTRING_INDEX(Owneraddress, ',', -1)
;

-- SPLIT OWNER NAME
SELECT 
    OwnerName,
    CASE
        WHEN OwnerName NOT LIKE '% AND %' THEN SUBSTRING_INDEX(OwnerName, '&', 1)
        ELSE OwnerName
    END AS OwnerName1, 
    CASE
        WHEN OwnerName LIKE '%&%' THEN SUBSTRING_INDEX(OwnerName, '&', - 1)
        ELSE ''
    END AS OwnerName2
FROM
    nashvillehousing;

-- CHANGE N TO NO AND Y TO YES IN SOLDASVACANT COLUMN

SELECT DISTINCT
    (soldasvacant), COUNT(soldasvacant)
FROM
    nashvillehousing
GROUP BY soldasvacant
ORDER BY 2 DESC
;

SELECT 
    soldasvacant,
    CASE
        WHEN soldasvacant = "Y" THEN "Yes"
        WHEN soldasvacant = "N" THEN "No"
        ELSE soldasvacant
    END as soldasvacant_fixed
FROM
    nashvillehousing
;

UPDATE nashvillehousing 
SET soldasvacant = CASE
        WHEN soldasvacant = 'Y' THEN 'Yes'
        WHEN soldasvacant = 'N' THEN 'No'
        ELSE soldasvacant
    END;

-- REMOVE DUPLICATES

DELETE FROM nashvillehousing
WHERE UniqueID IN (
	SELECT UniqueID 
    FROM (
		SELECT *, 
        ROW_NUMBER() OVER (PARTITION BY ParcelID, PropertyAddress, saledate, saleprice, legalreference) AS rownum
		FROM nashvillehousing
	) AS dups 
	WHERE rownum > 1
);

-- DELETE UNUSED COLUMNS

ALTER TABLE nashvillehousing
DROP COLUMN PropertyAddress,
DROP COLUMN OwnerAddress,
DROP COLUMN TaxDistrict
;



