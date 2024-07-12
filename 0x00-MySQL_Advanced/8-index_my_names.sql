-- Add column for first letter
ALTER TABLE names 
ADD COLUMN first_letter CHAR(1) GENERATED ALWAYS AS (SUBSTRING(name, 1, 1)) STORED;

-- Create index on first_letter column
CREATE INDEX idx_name_first ON names (first_letter);
