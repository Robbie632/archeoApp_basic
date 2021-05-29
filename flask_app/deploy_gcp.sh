
echo "building"
gcloud builds submit --tag gcr.io/semiotic-anvil-253215/$1 --project semiotic-anvil-253215
echo "deploying"
gcloud run deploy --image gcr.io/semiotic-anvil-253215/$1 --platform managed --project semiotic-anvil-253215
