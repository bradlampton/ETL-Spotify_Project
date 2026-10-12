import os
import io
import csv
import json
import urllib.parse
from datetime import datetime, timezone
import boto3

s3 = boto3.client('s3')

FIELDS = [
    'track_id', 'track_name', 'artists', 'album_id', 'album_name',
    'album_release_date', 'album_type', 'duration_ms', 'explicit',
    'popularity', 'track_number', 'track_url', 'source_file', 'processed_at'
]

def lambda_handler(event, context):
    print("VERSION CHECK: transform v1")
    processed = []

    for record in event.get('Records', []):
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        # Only handle valid JSON files
        if not key.endswith('.json'):
            print(f"Skipping non-JSON file: {key}")
            continue

        print(f"Reading s3://{bucket}/{key}")
        obj = s3.get_object(Bucket=bucket, Key=key)
        data = json.loads(obj['Body'].read().decode('utf-8'))

        items = data.get('tracks', {}).get('items', [])
        now = datetime.now(timezone.utc).isoformat()

        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=FIELDS)
        writer.writeheader()

        row_count = 0
        for t in items:
            if not t:
                continue
            album = t.get('album') or {}
            artists = t.get('artists') or []
            writer.writerow({
                'track_id': t.get('id'),
                'track_name': t.get('name'),
                'artists': '; '.join(a.get('name', '') for a in artists),
                'album_id': album.get('id'),
                'album_name': album.get('name'),
                'album_release_date': album.get('release_date'),
                'album_type': album.get('album_type'),
                'duration_ms': t.get('duration_ms'),
                'explicit': t.get('explicit'),
                'popularity': t.get('popularity'),  
                'track_number': t.get('track_number'),
                'track_url': (t.get('external_urls') or {}).get('spotify'),
                'source_file': key,
                'processed_at': now,
            })
            row_count += 1

        # Read environment variable for destination bucket
        out_bucket = os.environ.get('S3_TRANSFORMED_BUCKET', bucket)
        
        # Determine dynamic safe writing destination
        if 'raw_data/' in key:
            out_key = key.replace('raw_data/', 'processed_data/', 1)[:-5] + '.csv'
        else:
            out_key = f"processed_data/{key[:-5]}.csv"

        s3.put_object(
            Bucket=out_bucket,
            Key=out_key,
            Body=buffer.getvalue().encode('utf-8'),
            ContentType='text/csv'
        )
        print(f"Wrote {row_count} rows to s3://{out_bucket}/{out_key}")
        processed.append(out_key)

    return {'statusCode': 200, 'body': json.dumps({'files_written': processed})}
