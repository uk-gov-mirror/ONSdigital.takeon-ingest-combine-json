# takeon-ingest-combine-json
A lambda function to extract JSON files from s3 bucket takeon-ingest-ingestion-zone-bucket, combining the files into an array and pushing to the business layer and notification queue

# to run
Ensure there are files in the s3 bucket - look at takeon-ingest-pck-to-json repository - this populates the bucket. Running on AWS lambda, send empty JSON in a test event. Running from the editor, run file in terminal

