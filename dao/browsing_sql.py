INIT_SQL ="""\
CREATE TABLE IF NOT EXISTS "browsing_history" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"src_ip" TEXT,
"src_port" INTEGER,
"dst_ip" TEXT,
"dst_port" INTEGER,
"timestamp" TEXT,
"title" TEXT,
"url" TEXT,
"browsing_time" FLOAT
)
"""

INSERT_HTTP_COMMUNICATION = """\
INSERT INTO browsing_history
(src_ip, src_port, dst_ip, dst_port, timestamp, title, url)
VALUES
("{src_ip}", {src_port}, "{dst_ip}", {dst_port}, "{timestamp}", "{title}", "{url}")
"""

SELECT_FOR_BROWSING_TIME = """\
SELECT id, src_ip, timestamp FROM browsing_history
WHERE browsing_time IS NULL OR browsing_time = ''
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
WHERE browsing_time IS NOT NULL
"""

SEARCH_TMP = """\
SELECT {cols} FROM browsing_history
WHERE browsing_time IS NOT NULL
    AND (
        src_ip REGEXP '{keyword}'
        OR dst_ip REGEXP '{keyword}'
        OR src_port REGEXP '{keyword}'
        OR dst_port REGEXP '{keyword}'
        OR url REGEXP '{keyword}'
        OR title REGEXP '{keyword}'
    )
ORDER BY id DESC
"""
