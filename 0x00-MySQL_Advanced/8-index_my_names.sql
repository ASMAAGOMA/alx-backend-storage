-- index
ALTER TABLE names 
ADD COLUMN first_letter CHAR(1) GENERATED ALWAYS AS (SUBSTRING(name, 1, 1)) STORED;
CREATE INDEX letter ON names (first_letter);
