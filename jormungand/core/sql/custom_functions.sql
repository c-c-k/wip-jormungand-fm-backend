DROP FUNCTION IF EXISTS GET_AIRPORTS_BY_SUBSTRING;

CREATE OR REPLACE FUNCTION GET_AIRPORTS_BY_SUBSTRING(
    _substring text, _limit integer
)
-- Returns `_limit` top airports containing `_substring`
-- in their IATA code/country code/country name/principality/airport name.
RETURNS SETOF airports_join_countries AS $$
    WITH id_matches AS (
        SELECT airport_id
        FROM airports_search_strings
        WHERE search_string ILIKE ('%' ||
            regexp_replace(_substring, '([\%_])', '\\\1', 'g')
            || '%') ESCAPE '\'
        LIMIT _limit
    )
    SELECT *
    FROM airports_join_countries
    WHERE airport_id IN (SELECT airport_id FROM id_matches);
$$ LANGUAGE SQL;
