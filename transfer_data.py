from google.cloud import storage
import os

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
    transfer_data_to_gcs("results-bucket-fsfrfr", "mathconstruct_results", "mathconstruct_results")
