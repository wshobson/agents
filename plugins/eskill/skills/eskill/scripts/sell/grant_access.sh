#!/bin/bash
# grant_access.sh — Cấp / thu hồi quyền truy cập repo cho khách (bán access)
# Chạy: bash grant_access.sh grant <username>        # cấp quyền đọc
#       bash grant_access.sh revoke <username>       # thu hồi
#       bash grant_access.sh list                    # danh sách người có quyền
# Config qua .env cạnh script này (REPO=owner/name)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$HERE/.env"
REPO=""

[ -f "$ENV_FILE" ] && . "$ENV_FILE"
[ -z "$REPO" ] && { echo "LỖI: thiếu REPO trong $ENV_FILE (vd REPO=<owner>/<repo>)"; exit 1; }

action="${1:-}"
user="${2:-}"

case "$action" in
  grant)
    [ -z "$user" ] && { echo "Dùng: grant_access.sh grant <username>"; exit 2; }
    gh api -X PUT "repos/$REPO/collaborators/$user" -f permission=pull >/dev/null
    echo "[$(date +%Y-%m-%dT%H:%M:%S)] GRANT $user pull -> $REPO" >> "$HERE/access.log"
    echo "✅ Đã cấp quyền pull cho $user trên $REPO"
    ;;
  revoke)
    [ -z "$user" ] && { echo "Dùng: grant_access.sh revoke <username>"; exit 2; }
    gh api -X DELETE "repos/$REPO/collaborators/$user" >/dev/null || true
    echo "[$(date +%Y-%m-%dT%H:%M:%S)] REVOKE $user <- $REPO" >> "$HERE/access.log"
    echo "✅ Đã thu hồi quyền của $user"
    ;;
  list)
    gh api "repos/$REPO/collaborators?per_page=100" --jq '.[] | "\(.login) | \(.permissions.pull == true)"'
    ;;
  *)
    echo "Dùng: grant_access.sh {grant|revoke|list} [username]"
    exit 2
    ;;
esac
