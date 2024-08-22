-- create a stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE userId INT;
    DECLARE weighted_sum FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO userId;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- calculate weighted sum and total weight for each user
        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO weighted_sum, total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = userId;

        -- update average score for the user
        UPDATE users
        SET average_score = weighted_sum / total_weight
        WHERE id = userId;
    END LOOP;

    CLOSE cur;
END;
//
DELIMITER ;
