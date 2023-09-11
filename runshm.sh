source ~/.bashrc
for i in {1..100}; do
    sleep_duration=$(( RANDOM % 30 + 15 ))  # Generate a random sleep duration between 15 and 45 seconds
    echo "Sleeping for ${sleep_duration} seconds..."
    sleep ${sleep_duration}
    echo "Executing shaadi.py..."
    python shaadi.py
    echo "Executing js.py.."
    #python js.py 
done
