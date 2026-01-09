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
        <div class="row">
            <EventChart data={onTransient} {yMin} {yMax} showLegend={true} />
            <EventChart data={offTransient} {yMin} {yMax} off={true} />
        </div>
        <div class="row">
            <EventChart
                data={onExemplar}
                {yMin}
                {yMax}
                exemplar={true}
                showLegend={true}
            />
            <EventChart
                data={offExemplar}
                {yMin}
                {yMax}
                off={true}
                exemplar={true}
            />
        </div>
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
        /* height: 100%; */
        flex: 1;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .event-charts-container {
        display: flex;
        flex-wrap: wrap;
        flex-direction: column;
        width: 70%;
        /* margin-top: 10px; */
        /* margin-bottom: 10px; */
        /* background-color: blue; */
    }

    .row {
        display: flex;
        /* width: 100%; */
        flex: 1;
        border: 2px solid gray;
        border-radius: 10px;
        box-shadow: 3px 1px 4px #888;
        padding-left: 50px;
        padding-right: 50px;
        margin-left: 10px;
        margin-right: 10px;
        /* margin-bottom: 10px;
        margin-top: 10px; */
    }

    .row:first-child {
        margin-bottom: 5px;
    }

    .row:last-child {
        margin-top: 5px;
    }
</style>
