-- creates a stored procedure ComputeAverageWeightedScoreForUsers 
-- that computes and store the average weighted score for all students.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE totalUsers INT;

    SELECT COUNT(*) INTO totalUsers FROM users;
    
    WHILE i <= totalUsers DO
        UPDATE users
        SET average_score = (
            SELECT SUM(weight * score) / SUM(weight) 
            FROM corrections JOIN projects 
            ON project_id = id 
            WHERE corrections.user_id = i
        )
        WHERE id = i; 
        SET i = i + 1;
    END WHILE;
END;

//

DELIMITER ;
