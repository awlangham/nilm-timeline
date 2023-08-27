<script>
    import TimelineChart from "../charts/TimelineChart.svelte";

    export let selectedID;

    let start_ts, end_ts, loadData;

    let rangePromise = fetch("api/range")
        .then((response) => response.json())
        .then((j) => {
            start_ts = j.range_start / 1000;
            end_ts = j.range_end / 1000;
        });

    const getData = () => {
        fetch("api/data?start_ts=" + start_ts + "&end_ts=" + end_ts)
            .then((response) => response.json())
            .then((j) => {
                loadData = j.loads;
            });
    };
</script>

{#await rangePromise then}
    <TimelineChart
        bind:selectedID
        bind:start_ts
        bind:end_ts
        {loadData}
        on:update={getData}
    />
{/await}
