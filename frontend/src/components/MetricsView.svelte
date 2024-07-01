<script>
    export let metrics;
</script>

<div class="metrics-container">
    <p>Number of runs in previous 24h: {metrics.num_runs_24h}</p>
    <p>
        Average run duration in previous 24h: {Math.round(
            metrics.avg_run_duration,
        )} seconds
    </p>
    <p>
        Match score with exemplar: {(
            100 * metrics.distance_from_exemplar
        ).toFixed(1)}%
    </p>
</div>

<style>
    .metrics-container {
        text-align: center;
        width: 40%;
        margin-top: 10px;
        margin-left: auto;
        margin-right: auto;
        border: 2px solid gray;
        border-radius: 10px;
        box-shadow: 3px 1px 4px #888;
        background-color: white;
    }
</style>
