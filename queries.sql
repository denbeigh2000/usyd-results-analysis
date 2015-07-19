-- Number of CP per semester
SELECT semester, sum(cp) AS num_units
    FROM results
    GROUP BY semester
    ORDER BY num_units DESC;

-- Number of CP per year
SELECT ((semester_num-1)/2)+1 AS year, SUM(cp*mark)/SUM(cp) AS wam
    FROM results
    GROUP BY year
    ORDER BY year ASC;

-- Grade count per semester
SELECT grade, COUNT(grade), semester
    FROM results
    GROUP BY semester;

-- Grade count per year
SELECT grade, COUNT(grade), ((semester_num-1)/2)+1 AS year
    FROM results
    GROUP BY year, grade;

-- Grade count overall
SELECT COUNT(*) as grade_count, grade
    FROM results
    GROUP BY grade
    ORDER BY grade_count DESC;

-- WAM per semester
SELECT semester, SUM(mark*cp)/SUM(cp) AS wam
    FROM results
    GROUP BY semester;

-- WAM per year
SELECT ((semester_num-1)/2)+1 AS year, SUM(cp*mark)/SUM(cp) AS wam
    FROM results
    GROUP BY year;

-- WAM per faculty
SELECT SUM(mark*cp)/SUM(cp) AS wam, faculty, count(*)
    FROM (
        SELECT mark, RTRIM(code, '0123456789') AS faculty, cp
        FROM results
    )
    GROUP BY faculty
    ORDER BY wam DESC;

-- WAM overall
SELECT SUM(mark*cp)/SUM(cp) AS wam
    FROM results;

-- Top 5 subjects
SELECT mark, grade, subject
    FROM results
    ORDER BY mark DESC
    LIMIT 5;

-- Bottom 5 subjects
SELECT mark, grade, subject
    FROM results
    ORDER BY mark ASC
    LIMIT 5;

-- All subjects sorted by mark
SELECT mark, grade, subject
    FROM results;
    ORDER BY mark DESC;

