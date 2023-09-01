<script>
    import * as d3 from "d3";
    import EventChart from "../charts/EventChart.svelte";
    import DistanceInfo from "../DistanceInfo.svelte";

    export let selectedID;

    let transientPromise;

    let transient_timestamps,
        transient_P,
        transient_Q,
        exemplar_timestamps,
        exemplar_P,
        exemplar_Q,
        selectedDistance,
        selectedNumDailyRuns;

    const colorScale = d3.scaleOrdinal(["P", "Q"], d3.schemeTableau10);

    $: if (selectedID != -1) {
        transientPromise = fetch("api/event/" + selectedID)
            .then((response) => response.json())
            .then((j) => {
                transient_timestamps = j.transient.timestamps;
                transient_P = j.transient.P;
                transient_Q = j.transient.Q;

                exemplar_timestamps = j.exemplar.timestamps;
                exemplar_P = j.exemplar.P;
                exemplar_Q = j.exemplar.Q;

                selectedDistance = j.distance;
                selectedNumDailyRuns = j.num_daily_runs;
            });
    }
</script>

<button
    id="back-btn"
    on:click={() => {
        selectedID = -1;
    }}
>
    Back
</button>

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

    <DistanceInfo distance={selectedDistance} numDailyRuns={selectedNumDailyRuns} />
{/await}

<style>
    #back-btn {
        position: absolute;
        top: 10px;
        left: 15px;
        font-family: sans-serif;
        font-size: 24px;
    }
</style>
