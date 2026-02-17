#!/bin/bash

# Load application configuration
load_config() {
    local env_file=".env"

    if [ ! -f "$env_file" ]; then
        echo "ERROR" "Configuration file '$env_file' not found."
        return 1
    fi

    if export $(grep -v '^#' "$env_file" | xargs) > /dev/null 2>&1; then
        echo "INFO" "Application configuration has been loaded successfully."
    fi
}



# Start Celery worker with beat scheduler
start_celery_worker() {
    local app_name="services.jobs.${TASK_APP}.celery"
    local schedule_file="/tmp/celerybeat-${TASK_APP}.db"
    
    echo "INFO: Starting Celery worker for ${TASK_APP}"
    
    # Start Celery with file-based scheduler
    celery -A "${app_name}" worker -E \
        --beat \
        --loglevel="info" \
        --schedule="${schedule_file}"
}

# Main execution
main() {
    load_config || exit 1
    start_celery_worker
}

main "$@"