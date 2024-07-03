<script>
    import TimelineChart from "../charts/TimelineChart.svelte";

    export let selectedInterval;

    let start_ts, end_ts, loadData, loadNames;

    let rangePromise = fetch("api/range")
        .then((response) => response.json())
        .then((j) => {
            start_ts = j.range_start / 1000;
            end_ts = j.range_end / 1000;
        });

    const getData = () => {
        const padding = Math.max(end_ts - start_ts, 30 * 60e6);

        fetch(
            "api/data?start_ts=" +
                (start_ts - padding) +
                "&end_ts=" +
                (end_ts + padding),
        )
            .then((response) => response.json())
            .then((j) => {
                loadData = j.loads;
                loadNames = j.labels.sort();
            });
    };
</script>

{#await rangePromise then}
    <TimelineChart
        bind:selectedInterval
        bind:start_ts
        bind:end_ts
        {loadData}
        {loadNames}
        on:update={getData}
    />
{/await}
