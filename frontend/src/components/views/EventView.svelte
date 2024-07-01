<script>
    import * as d3 from "d3";
    import EventChart from "../charts/EventChart.svelte";
    import MetricsView from "../MetricsView.svelte";

    export let selectedTimestamp;

    let transientPromise;

    let transient_timestamps,
        transient_P,
        transient_Q,
        exemplar_timestamps,
        exemplar_P,
        exemplar_Q,
        metrics;

    const colorScale = d3.scaleOrdinal(["P", "Q"], d3.schemeTableau10);

    $: if (selectedTimestamp != -1) {
        transientPromise = fetch("api/event/" + selectedTimestamp)
            .then((response) => response.json())
            .then((j) => {
                transient_timestamps = j.transient.timestamps;
                transient_P = j.transient.P;
                transient_Q = j.transient.Q;

                if (j.exemplar) {
                    exemplar_timestamps = j.exemplar.timestamps;
                    exemplar_P = j.exemplar.P;
                    exemplar_Q = j.exemplar.Q;
                }

                metrics = j.metrics;
            });
    }
</script>

<button
    id="back-btn"
    on:click={() => {
        selectedTimestamp = -1;
    }}
>
    Back
</button>

<div class="event-view-container">
    {#await transientPromise then}
        <EventChart
            x1={transient_timestamps}
            y1={transient_P}
            c1={colorScale("P")}
            x2={exemplar_timestamps}
            y2={exemplar_P}
            yAxisLabel="Active Power (kW)"
        />

        <EventChart
            x1={transient_timestamps}
            y1={transient_Q}
            c1={colorScale("Q")}
            x2={exemplar_timestamps}
            y2={exemplar_Q}
            yAxisLabel="Reactive Power (kVar)"
        />

        <MetricsView {metrics} />
    {/await}
</div>

<style>
    #back-btn {
        position: absolute;
        top: 20px;
        left: 25px;
        font-family: sans-serif;
        font-size: 24px;
    }

    .event-view-container {
        display: flex;
        flex-wrap: wrap;
        margin-top: 10px;
    }
</style>
