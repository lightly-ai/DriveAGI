#!/bin/bash


#MAXID=2113 # Maximum train video id.
STARTID=0
MAXID=2113
BATCHSIZE=2

process_videos() {
    STARTID=$1
    ENDID=$(($1 + $BATCHSIZE - 1))  # Calculate end of range, i+9

    # Check if ENDID exceeds MAXID and adjust if necessary
    if [ $ENDID -gt $MAXID ]; then
        ENDID=$MAXID
    fi

    # Prepare the arguments string with IDs after the -v flag
    args="-v"
    for (( j=STARTID; j<=ENDID; j++ )); do
        args+=" $j"
    done

    # Download and preprocess data
    python scripts/meta_preprocess.py $args
    python scripts/youtube_download.py >> download_output.txt

    aws s3 cp --recursive OpenDV-YouTube/videos/ s3://lightly-datasets/lotwheels2/videos/$STARTID_$ENDID/ --dry-run

    # Remove the downloaded videos and frames
    rm -rf OpenDV-YouTube/videos
    rm -rf OpenDV-YouTube/full_images
}

# Loop through all the IDs in batches of 10
for (( id=STARTID; id<=MAXID; id+=BATCHSIZE ))
do
    process_videos $id  # Pass the current id to the function
done
