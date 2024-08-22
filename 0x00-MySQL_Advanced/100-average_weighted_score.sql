-- create a stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE weighted_sum FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    -- calculate weighted sum and total weight
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO weighted_sum, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- update average score for the user
    UPDATE users
    SET average_score = weighted_sum / total_weight
    WHERE id = user_id;
END;
//
DELIMITER ;
