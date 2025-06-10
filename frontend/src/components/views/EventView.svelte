<script>
    import EventChart from "../charts/EventChart.svelte";
    import MetricsView from "../MetricsView.svelte";

    export let selectedInterval;

    let transientPromise;

    let onTransient, offTransient, onExemplar, offExemplar, loadName, metrics;

    const onKeyPress = (e) => {
        if (e.keyCode === 27) {
            selectedInterval = [];
        }
    };

    let allData = [];
    $: if (onTransient && offTransient && onExemplar && offExemplar) {
        allData = onTransient["P"].concat(
            onTransient["Q"],
            offTransient["P"],
            offTransient["Q"],
            onExemplar["P"],
            onExemplar["Q"],
            offExemplar["P"],
            offExemplar["Q"],
        );
    }

    $: yMin = Math.min(...allData);
    $: yMax = Math.max(...allData);

    transientPromise = fetch(
        "api/event/" + selectedInterval[0] + "/" + selectedInterval[1],
    )
        .then((response) => response.json())
        .then((j) => {
            onTransient = j.on_transient;
            offTransient = j.off_transient;

            onExemplar = j.on_exemplar;
            offExemplar = j.off_exemplar;

            loadName = j.load_name;
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

<div class="event-view-container">
    <div class="event-charts-container">
        <EventChart
            data={onTransient}
            {yMin}
            {yMax}
            yAxisLabel="Selected ON"
            showLegend={true}
        />
        <EventChart
            data={offTransient}
            {yMin}
            {yMax}
            off={true}
            yAxisLabel="Selected OFF"
        />
        <EventChart data={onExemplar} {yMin} {yMax} yAxisLabel="Exemplar ON" />
        <EventChart
            data={offExemplar}
            {yMin}
            {yMax}
            off={true}
            yAxisLabel="Exemplar OFF"
        />
    </div>
    {#await transientPromise then}
        <MetricsView {loadName} {metrics} />
    {/await}
</div>

<svelte:window on:keydown={onKeyPress} />

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
        width: 70%;
        margin-top: 10px;
    }
</style>
