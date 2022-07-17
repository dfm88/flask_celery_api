job_id="$1"
echo "received $job_id"
curl --location --request GET "http://localhost:5000/task_status/$job_id"