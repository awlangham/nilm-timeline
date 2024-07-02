<script>
    import { fade } from "svelte/transition";
    import { formatSeconds } from "./charts/utilities";

    export let loadName, metrics;
</script>

<div class="metrics-container" in:fade>
    <h1>{loadName}</h1>

    <p>Number of runs in previous 24h: {metrics.num_runs_24h}</p>

    <p>
        {#if metrics.avg_run_duration}
            Average run duration in previous 24h: {formatSeconds(metrics.avg_run_duration)}
        {:else}
            No runs in previous 24h
        {/if}
    </p>
    <p>
        ON match score: {(
            100 *
            (1 - metrics.on_distance)
        ).toFixed(1)}%
    </p>

    <p>
        OFF match score: {(
            100 *
            (1 - metrics.off_distance)
        ).toFixed(1)}%
    </p>
</div>

<style>
    .metrics-container {
        text-align: center;
        width: 30%;
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: auto;
        margin-right: auto;
        border: 2px solid gray;
        border-radius: 10px;
        box-shadow: 3px 1px 4px #888;
        background-color: white;
    }
</style>
