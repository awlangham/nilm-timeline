<script>
    export let metrics;
</script>

<div>
    <p>Number of runs in previous 24h: {metrics.num_runs_24h}</p>
    <p>Average run duration in previous 24h: {Math.round(metrics.avg_run_duration)} seconds</p>
    <p>Match score with exemplar: {(100 * metrics.distance_from_exemplar).toFixed(1)}%</p>
</div>
