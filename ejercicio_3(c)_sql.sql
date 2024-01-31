WITH UsuariosOrdenados AS (
 SELECT user_id, course_id, enrollment_date,
    ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY enrollment_date ASC) AS Ranking
 FROM cursos
)
SELECT user_id, course_id, enrollment_date
FROM UsuariosOrdenados
WHERE Ranking <= 3;