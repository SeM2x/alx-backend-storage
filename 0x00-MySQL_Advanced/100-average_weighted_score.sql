-- creates a stored procedure ComputeAverageWeightedScoreForUser 
-- that computes and store the average weighted score for a student.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
  IN user_id INT
)
BEGIN
  UPDATE users
  SET average_score = (
    SELECT SUM(weight * score) / SUM(weight) 
    FROM corrections JOIN projects 
    ON project_id = id 
    WHERE corrections.user_id = user_id
    )
  WHERE id = user_id; 
END;

//

DELIMITER ;
