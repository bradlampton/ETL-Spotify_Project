import os
import json
import base64
from datetime import datetime
import urllib.request
import urllib.parse
import boto3

def lambda_handler(event, context):
    client_id = os.environ.get('SPOTIFY_CLIENT_ID', '').strip()
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET', '').strip()
    bucket_name = os.environ.get('S3_RAW_BUCKET')
    
    if not client_id or not client_secret:
        return {'statusCode': 500, 'body': 'CRITICAL ERROR: Environment variables are empty!'}
        
    print(f"Diagnostic -> ID Length: {len(client_id)}, Secret Length: {len(client_secret)}")

    try:
        # Base64 Encode Credentials for Client Credentials Flow
        auth_string = f"{client_id}:{client_secret}"
        auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        
        token_url = "https://accounts.spotify.com/api/token"
        token_data = urllib.parse.urlencode({'grant_type': 'client_credentials'}).encode('utf-8')
        token_headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        token_req = urllib.request.Request(token_url, data=token_data, headers=token_headers, method='POST')
        
        try:
            with urllib.request.urlopen(token_req) as response:
                token_response = json.loads(response.read().decode('utf-8'))
                access_token = token_response['access_token']
        except urllib.error.HTTPError as e:
            raw_error = e.read().decode('utf-8')
            return {
                'statusCode': e.code,
                'body': f"Spotify Token Endpoint Explicitly Rejected Request! Raw Message: {raw_error}"
            }

        # Fetch Data from Public Search Endpoint (Genre: Pop)
        playlist_url = "https://api.spotify.com/v1/search?q=genre%3Apop&type=track&limit=10"
        playlist_headers = {"Authorization": f"Bearer {access_token}"}
        playlist_req = urllib.request.Request(playlist_url, headers=playlist_headers, method='GET')
        
        with urllib.request.urlopen(playlist_req) as response:
            spotify_data = json.loads(response.read().decode('utf-8'))
            
        # Deliver payload to Amazon S3 Raw Bucket
        s3_client = boto3.client('s3')
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_key = f"raw_data/spotify_raw_{current_time}.json"
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(spotify_data),
            ContentType='application/json'
        )
        
        return {
            'statusCode': 200,
            'body': f"Success! 10 tracks saved to s3://{bucket_name}/{file_key}"
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Unhandled Pipeline Exception: {str(e)}"
        }
