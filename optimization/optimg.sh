#!/bin/bash

# Small script that rebuilds a given filesystem-image into a new filesystem, with files in configurable order.
# Usage:
#   fsopt.sh [source-device or image] [dest-device or image] < [file-order or /dev/null]

HERE="$(dirname "$0")"
SRCIMG="$1"
DSTIMG="$2"
SRCMNT="/tmp/fsopt-src"
DSTMNT="/tmp/fsopt-dst"

function cleanup() {
  umount -lf "$SRCMNT" "$DSTMNT"
}
trap cleanup EXIT

mkdir -p "$SRCMNT" "$DSTMNT"
FS_UUID=$(blkid -s UUID -o value "$SRCIMG")
mkfs.ext4 "$DSTIMG" -U $FS_UUID

mount "$SRCIMG" "$SRCMNT" || exit
mount "$DSTIMG" "$DSTMNT" || exit

$HERE/mergelist.py "$SRCMNT" | $HERE/orderedcopy.py "$SRCMNT" "$DSTMNT"

