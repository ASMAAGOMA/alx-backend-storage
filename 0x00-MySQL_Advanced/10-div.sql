-- function
DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS DECIMAL(10, 4)
DETERMINISTIC
BEGIN
    DECLARE result DECIMAL(10, 4);

    -- Handle NULL inputs
    IF a IS NULL OR b IS NULL THEN
        SET result = NULL;  -- or handle as appropriate
    ELSE
        IF b = 0 THEN
            SET result = 0;
        ELSE
            SET result = a / b;
        END IF;
    END IF;

    RETURN result;
END$$
DELIMITER ;
