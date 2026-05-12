<script>
    import { fade } from "svelte/transition";
    // import { formatSeconds } from "./charts/utilities";
    import Gauge from "./Gauge.svelte";
    import Phasor from "./Phasor.svelte";

    export let loadName, metrics;
</script>

<div in:fade>
    <h1>{loadName}</h1>

    <p>Number of runs in previous 24h: {metrics.num_runs_24h}</p>

    <!-- <p>
        {#if metrics.avg_run_duration}
            Average run duration in previous 24h: {formatSeconds(
                metrics.avg_run_duration,
            )}
        {:else}
            No runs in previous 24h
        {/if}
    </p> -->
    <p>
        ON match score: {(100 * (1 - metrics.on_distance)).toFixed(1)}%
    </p>

    <p>
        OFF match score: {(100 * (1 - metrics.off_distance)).toFixed(1)}%
    </p>

    <Gauge
        nominalValue={metrics.P_ss_nom}
        actualValue={metrics.P_ss_seen}
        label="Steady-State P (W)"
    ></Gauge>

    <Gauge
        nominalValue={metrics.Q_ss_nom}
        actualValue={metrics.Q_ss_seen}
        label="Steady-State Q (Var)"
    ></Gauge>

    <div>
        <Phasor observed={metrics.zero_seen} nominal={metrics.zero_nom} threshold={metrics.threshold}
        ></Phasor>
    </div>
</div>
