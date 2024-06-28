<script>
    export let metrics;
</script>

<div>
    <p>Number of runs in previous 24h: {metrics.num_runs_24h}</p>
    <p>Average run duration in previous 24h: {Math.round(metrics.avg_run_duration)} seconds</p>
</div>
