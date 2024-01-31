WITH CalificacionesOrdenadas AS (
 SELECT user_id, course_id, grade,
    ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY grade DESC) AS Ranking
 FROM cursos
)
SELECT user_id, course_id, grade FROM CalificacionesOrdenadas WHERE Ranking <= 3;