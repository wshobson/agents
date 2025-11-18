#!/bin/bash
# ceph-health-check.sh - Check Ceph cluster health

echo "=== Ceph Cluster Health ==="
ceph -s

echo -e "\n=== OSD Status ==="
ceph osd stat

echo -e "\n=== PG Status ==="
ceph pg stat

echo -e "\n=== Pool Usage ==="
ceph df

echo -e "\n=== Slow Operations ==="
ceph -w | head -20
