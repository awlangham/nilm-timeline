<script>
    import EventChart from "../charts/EventChart.svelte";
    import MetricsView from "../MetricsView.svelte";

    export let selectedInterval;

    let transientPromise;

    let onTransient, offTransient, onExemplar, offExemplar, metrics;

    transientPromise = fetch(
        "api/event/" + selectedInterval[0] + "/" + selectedInterval[1],
    )
        .then((response) => response.json())
        .then((j) => {
            onTransient = j.on_transient;
            offTransient = j.off_transient;

            onExemplar = j.on_exemplar;
            offExemplar = j.off_exemplar;

            metrics = j.metrics;
        });
</script>

<button
    id="back-btn"
    on:click={() => {
        selectedInterval = [];
    }}
>
    Back
</button>

{#await transientPromise then}
    <div class="event-view-container">
        <div class="event-charts-container">
            <EventChart data={onTransient} yAxisLabel="Selected ON" />
            <EventChart data={offTransient} yAxisLabel="Selected OFF" />
            <EventChart data={onExemplar} yAxisLabel="Exemplar ON" />
            <EventChart data={offExemplar} yAxisLabel="Exemplar OFF" />
        </div>

        <MetricsView {metrics} />
    </div>
{/await}

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
    }

    .event-charts-container {
        display: flex;
        flex-wrap: wrap;
        width: 60%;
        margin-top: 10px;
    }
</style>
