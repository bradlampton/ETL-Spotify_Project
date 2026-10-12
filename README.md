# Spotify End-to-End Serverless Data Pipeline

An automated, event-driven data engineering pipeline built using Python and AWS Serverless services to extract, transform, and analyze streaming tracking statistics from the Spotify Web API.

## 📌 Architecture Topology
```
[Spotify API]
       │ (3x / Week Trigger via EventBridge Cron)
       ▼
[AWS Lambda (Extract)] ────► [Amazon S3 (Landing Zone: Raw JSON)]
                                        │
                                        ▼ (S3 PutObject Automation Event)
                          [AWS Lambda (Transform)] ────► [Amazon S3 (Target Zone: Clean CSV)]
                                                                    │
                                                                    ▼
                                                           [AWS Glue Crawler]
                                                                    │
                                                                    ▼
                                                           [Amazon Athena (SQL)]
```

## 🛠️ Infrastructure Component Matrix
* **Language/Compute:** Python 3.11 Execution Environment executed serverless via AWS Lambda.
* **Storage Layers:** Isolated multi-tier landing architecture inside Amazon S3 (Raw Landings vs Processed Analytics targets).
* **Workflow Orchestration:** Amazon EventBridge Cron scheduler running automated pipelines on a customized interval.
* **Metadata Schema Cataloging:** AWS Glue Crawler dynamically evaluating structural CSV mutations into data catalogs.
* **SQL Query Engine:** Amazon Athena providing decoupled ad-hoc analytics directly across distributed storage layers.

## 📁 Repository Manifest
```text
├── extract.py         # Lambda Handler: API Tokenization & raw JSON streaming dumps
├── transform.py       # Lambda Handler: Event-Driven flattening layer & analytical CSV formatting
└── README.md          # Comprehensive architecture layout documentation
```

## 🚀 Execution Configurations

### 1. Extraction Security Context
Attach these explicit keys inside your environment configurations dashboard (`extract.py` context):
* `SPOTIFY_CLIENT_ID`: Standard 32-character hexadecimal developer key token.
* `SPOTIFY_CLIENT_SECRET`: Standard 32-character encryption token string.
* `S3_RAW_BUCKET`: Target landing zone bucket naming reference (`bradlampton-spotify-raw`).

### 2. Transformation Context
Configure these targets inside your transformation container dashboard context (`transform.py` execution layer):
* `S3_TRANSFORMED_BUCKET`: Target relational processing store (`bradlampton-spotify-transformed`).

### 3. Orchestration Trigger Cadence
To maintain a production-ready interval, use this EventBridge Schedule Cron pattern to lock in execution 3 times a week (Mon, Wed, Fri at 12:00 PM UTC):
```text
0 12 ? * MON,WED,FRI *
```
