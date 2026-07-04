An Apache-style access log is at `/app/access.log`. Parse it and write a JSON summary report to `/app/out.json`.

## Success criteria

1. Create `/app/out.json` containing valid JSON with exactly these keys:
   - `total_requests` (integer): total number of log lines (non-empty lines count as one request).
   - `unique_ips` (integer): number of distinct client IP addresses (the first field on each line).
   - `top_path` (string): the request path that appears most often (extract from the quoted `"METHOD /path HTTP/..."` segment; break ties by choosing any path with the maximum count).
2. Values must reflect the actual contents of `/app/access.log`, not placeholder or hard-coded numbers.
