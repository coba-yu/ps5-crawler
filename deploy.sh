poetry export -f requirements.txt --output src/requirements.txt --without-hashes

# https://cloud.google.com/sdk/gcloud/reference/auth/login
gcloud auth login yuu.meiji.research@gmail.com

PROJECT_ID='spry-pier-279201'

# https://cloud.google.com/sdk/gcloud/reference/functions/deploy
gcloud functions deploy \
  ps5-crawler \
  --region=asia-northeast1 \
  --set-build-env-vars='LINE_NOTIFY_ACCESS_TOKEN=1rKprAC1sKGT49f8ZiwH6VsjLQFhbMjqnSFLnI577gz' \
  --entry-point='main' \
  --memory=512MB \
  --runtime 'python39' \
  --trigger-topic 'hourly' \
  --service-account="${PROJECT_ID}@appspot.gserviceaccount.com" \
  --source='src' \
  --stage-bucket='cf-src' \
  --project ${PROJECT_ID}
