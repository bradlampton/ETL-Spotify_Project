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
## 🟦 Enterprise Business Intelligence Layer (Microsoft Power BI)

To translate complex data lakehouse infrastructure into actionable business insights, a professional analytics reporting layer was deployed using **Microsoft Power BI Desktop**. The architecture leverages a serverless cloud-federated model, connecting Power BI straight to the **Amazon Athena** query execution engine in the native `us-east-2` AWS region via a secure gateway tunnel.

### ⚡ Architectural Performance Tuning & Optimization

A primary challenge with multi-cloud architectures is eliminating data replication latency while controlling serverless processing overhead. Standard BI dataset ingestion requires scheduled import loops that scan the entire history of an S3 storage bucket, racking up significant data scanning compute costs.

To solve this, the reporting layer was built using an optimized **DirectQuery Custom SQL Connection Block** injected directly at the ingestion gate. This ensures zero local caching storage overhead (0 MB footprint), with all computations pushed downstream to AWS's distributed compute layer in real time.

```sql
SELECT 
    track_id,
    track_name,
    artists,
    album_name,
    album_release_date,
    TRY_CAST(popularity AS INT) as popularity,
    processed_at,
    source_file
FROM "spotify_analytics"."processed_data"
WHERE processed_at >= CAST(date_add('day', -7, current_date) AS VARCHAR)
ORDER BY popularity DESC
```

### 🧠 Performance Engineering Breakthroughs

* **Sliding-Window Partitioning:** By establishing an active 7-day sliding data window filter (`WHERE processed_at >= ...`), the query engine bypasses cold historical archives on S3. This limits the data scan layout exclusively to the most recent pipeline runs, minimizing serverless runtime compute charges.
* **Source-Level Type Conversion:** Implementing `TRY_CAST(popularity AS INT)` directly within Presto SQL ensures formatting execution happens inside AWS before cross-cloud transit, preventing local dashboard rendering bottlenecks.
* **Pure Cloud-Federated Architecture:** Operating in true **DirectQuery Mode** ensures that every dashboard interaction triggers an instantaneous, secure round-trip API call down through an **On-Premises Data Gateway** straight to AWS, serving live metrics with zero local caching requirements.

---

### 🎨 Implemented Executive Visualizations

The public interactive report canvas features three strategic components engineered to track both music popularity trends and backend pipeline reliability parameters:

1. **The Popularity Leaderboard (Clustered Bar Chart):** Maps track names dynamically against max calculation popularity metrics, sorting track rankings in descending order to surface the highest-velocity assets currently streaming in the lakehouse.
2. **Artist Concentration Density (Donut Chart):** Captures record count frequencies partitioned across primary artists to measure dataset distribution volume across automated data ingest cycles.
3. **Data Refresh Pulse Scorecard (Multi-Row Card):** Serves as a vital data engineering reliability tracker, printing the explicit, unique raw execution file keys (`source_file`) alongside live cleaning timestamps (`processed_at`) completely on autopilot.

---

## 🔗 Live Interactive Link
👉 **[View the Live Interactive Power BI Dashboard Portfolio Report]
    ((https://shorturl.at/fIyf8))**
*(No sign-in or Microsoft account required. Real-time data streams are routed live through the custom AWS gateway connection).*

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

Tableau Dashboard Layout Enhancements
Link to public Tableau dashboard: https://public.tableau.com/app/profile/brad.criss.lampton

To improve usability and presentation, each visualization was configured with optimal Tableau sizing settings:

Duration Leaderboard → Set to Entire View to maximize chart space, display full track names, and eliminate unnecessary scrolling.
Artist Concentration Density → Set to Entire View to automatically scale the pie chart, making artist distribution easier to interpret at a glance.
Pipeline Pulse Log List → Set to Fit Width to ensure ETL log details and source file names remain fully visible while preserving vertical scrolling for historical execution records.

These adjustments create a cleaner, more professional dashboard experience, improving readability, visual impact, and overall user interaction for portfolio and recruiter demonstrations.

