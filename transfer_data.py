from google.cloud import storage
import os
import argparse
def transfer_data_to_gcs(bucket_name, source_dir, destination_prefix=""):
    """
    Uploads an entire directory to the bucket.
    
    Args:
        bucket_name: The name of the GCS bucket
        source_dir: Local directory path to upload
        destination_prefix: Prefix for the destination in GCS (like a folder)
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    print(f"Uploading {source_dir} to {bucket_name}/{destination_prefix}")
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            local_file_path = os.path.join(root, file)
            
            # Determine the blob path in GCS
            relative_path = os.path.relpath(local_file_path, source_dir)
            blob_path = os.path.join(destination_prefix, relative_path).replace("\\", "/")
            
            # Create blob and upload file
            blob = bucket.blob(blob_path)
            blob.upload_from_filename(local_file_path)
            print(f"Uploaded {local_file_path} to {blob_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--list_buckets", action="store_true")
    args = parser.parse_args()
    if args.list_buckets:
        storage_client = storage.Client()
        buckets = storage_client.list_buckets()
        for bucket in buckets:
            print(bucket.name)
    else:
        transfer_data_to_gcs("results-bucket-fsfrfr", "mathconstruct_results", "mathconstruct_results")
