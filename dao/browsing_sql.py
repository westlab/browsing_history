INIT_Maria = """\
CREATE TABLE IF NOT EXISTS browsing_history (
  id int(11) NOT NULL AUTO_INCREMENT,
  src_ip varchar(255) NOT NULL,
  dst_ip varchar(255) NOT NULL,
  src_port int(11) NOT NULL,
  dst_port int(11) NOT NULL,
  timestamp datetime NOT NULL,
  title text,
  url text,
  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  browsing_time float,
  download int(11),
  PRIMARY KEY (id),
  KEY index_browsing_history_on_timestamp (timestamp),
  KEY index_browsing_history_on_src_ip (src_ip)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

INSERT_HTTP_COMMUNICATION = """\
INSERT INTO browsing_history
(src_ip, src_port, dst_ip, dst_port, timestamp, title, url)
VALUES
("{src_ip}", {src_port}, "{dst_ip}", {dst_port}, "{timestamp}", "{title}", "{url}")
"""

SELECT_FOR_BROWSING_TIME = """\
SELECT id, src_ip, timestamp FROM browsing_history
WHERE (browsing_time IS NULL OR browsing_time = '') AND
  created_at > '{timeout}'
"""

UPDATE_BROWSING_TIME="""\
UPDATE browsing_history
SET browsing_time = '{browsing_time}'
WHERE id = {id}
"""

SELECT_TMP = """\
SELECT {cols} FROM browsing_history
WHERE browsing_time IS NOT NULL
ORDER BY id DESC
LIMIT {limit}
"""

SELECT_WHERE = """\
SELECT {cols} FROM browsing_history
WHERE browsing_time IS NOT NULL AND {condition}
ORDER BY id DESC
LIMIT {limit}
"""

COUNT = """\
SELECT COUNT(*) FROM browsing_history
WHERE browsing_time IS NOT NULL
"""

COUNT_WHERE = """\
SELECT COUNT(*) FROM browsing_history
WHERE browsing_time IS NOT NULL AND {condition}
"""

DOMAIN = """\
SELECT url FROM browsing_history
WHERE browsing_time IS NOT NULL AND
  timestamp > '{lower_bound}'
"""

SRCIP = """\
SELECT src_ip FROM browsing_history
WHERE browsing_time IS NOT NULL AND
  timestamp > '{lower_bound}'
"""

SEARCH_TMP = """\
SELECT {cols} FROM browsing_history
WHERE browsing_time IS NOT NULL
    AND (
        src_ip REGEXP '{keyword}'
        OR url REGEXP '{keyword}'
        OR title REGEXP '{keyword}'
    )
ORDER BY id DESC
"""

LAST_BROWSING_BY_SRC_IP = """\
SELECT id, src_ip, timestamp
FROM browsing_history
WHERE browsing_time IS NOT NULL AND
  src_ip = '{src_ip}'
ORDER BY id DESC
LIMIT 1
"""

HISTOGRAM = """\
SELECT
{count_condition}
FROM (SELECT timestamp FROM browsing_history WHERE timestamp > '{max_time}') AS timestamp_groups
"""

HISTOGRAM_COUNT_FMT = """\
COUNT(CASE WHEN timestamp >= '{t_from}' AND timestamp < '{to}' THEN 1 END) AS '{label}'
"""