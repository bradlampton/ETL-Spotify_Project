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
markdown
## 📊 Business Intelligence & Visualization (Google Looker Studio)

To provide data consumers with an interactive analytical interface, the serverless data lakehouse is directly integrated with **Google Looker Studio**. This allows for zero-cost, real-time business intelligence dashboarding querying data hosted natively inside Amazon S3 via the Amazon Athena execution engine.

### 🛠️ Step-by-Step Connection Guide

Follow these steps to establish a secure data bridge from AWS to Google Looker Studio:

#### 1. Provision IAM Access Credentials
Looker Studio requires read access to your AWS Data Catalog and S3 buckets. 
1. Open the [AWS IAM Console](https://amazon.com).
2. Navigate to **Users** and click on your active deployment user profile.
3. Select the **Security credentials** tab and click **Create access key**.
4. Choose **Application running outside AWS**, click **Next**, and download the generated `.csv` credentials file containing your **Access Key ID** and **Secret Access Key**.

#### 2. Establish Data Source Mapping
1. Navigate to [Google Looker Studio](https://google.com) and click **Create** > **Data Source**.
2. In the connector search bar, type **Amazon Athena** and select the connector.
3. Provide your secure authentication parameters:
   * **AWS Access Key ID:** `YOUR_ACCESS_KEY`
   * **AWS Secret Access Key:** `YOUR_SECRET_KEY`
4. Set up the structural endpoint parameters using the dropdown selections:
   * **Region:** `us-east-2` *(or your primary AWS deployment region)*
   * **Catalog:** `AwsDataCatalog`
   * **Database:** `spotify_analytics`
   * **Table:** `processed_data`
5. Click **Connect** in the upper right corner to fetch the metadata schema layout.

---

### 🎨 Recommended Dashboard Metrics & Configuration

To effectively monitor your automated music ingest architecture, configure these foundational widgets on your visualization canvas:

#### A. The Popularity Leaderboard (Bar Chart)
* **Dimension:** `track_name`
* **Breakdown Dimension:** `artists`
* **Metric:** `popularity` (Set aggregation parameter to `MAX`)
* **Sort:** `popularity` (Descending)
* *Insight:* Captures the highest-performing tracking assets ingested by the pipeline.

#### B. Artist Market Share Analysis (Pie/Donut Chart)
* **Dimension:** `artists`
* **Metric:** `Record Count` (Aggregation: `COUNT`)
* *Insight:* Visualizes artist frequency across automated execution cycles.

#### C. Operational Data Pipeline Pulse (Scorecard)
* **Metric:** `source_file` (Change aggregation to `COUNT DISTINCT`)
* **Text Label:** `Total Automated Pipeline Runs`
* *Insight:* Serves as a vital data engineering metric, confirming that your Amazon EventBridge cron schedules are firing, processing files, and mutating your cloud storage layer completely on autopilot over time.

---

## 🔒 Production Security Best Practices (For Portfolios)
> ⚠️ **CRITICAL SECURITY NOTE:** Never commit your raw AWS Access Keys or Secret Keys directly into your public Git source tracking repositories. Ensure your `.env` tracking controls are safely registered inside your `.gitignore` settings to prevent cloud authentication exposures.

