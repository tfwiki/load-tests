#!/bin/bash


if [ -z "$TARGET_HOST" ] ; then
        echo "Required variable TARGET_HOST not set"
        missing_vars=true
fi

if [ -z "$LOCUST_MODEL" ] ; then
        echo "Required variable LOCUST_MODEL not set"
        missing_vars=true
fi

if [ "$missing_vars" = true ] ; then
    echo "Required variables are not set. See above for details."
    exit 1
fi

LOCUST="/usr/local/bin/locust"
LOCUS_OPTS="-f /load-test/$LOCUST_MODEL.py --host=$TARGET_HOST"
LOCUST_MODE=${LOCUST_MODE:-standalone}

if [[ "$LOCUST_MODE" = "master" ]]; then
    LOCUS_OPTS="$LOCUS_OPTS --master"
elif [[ "$LOCUST_MODE" = "worker" ]]; then
    LOCUS_OPTS="$LOCUS_OPTS --slave --master-host=$LOCUST_MASTER"
fi

echo "$LOCUST $LOCUS_OPTS"

$LOCUST $LOCUS_OPTS