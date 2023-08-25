<script>
    import TimelineChart from "../charts/TimelineChart.svelte";

    export let selectedID;

    let start_ts, end_ts, loadData;

    const getData = () => {
        fetch("api/data?start_ts=" + start_ts + "&end_ts=" + end_ts)
            .then((response) => response.json())
            .then((j) => {
                loadData = j.loads;
            });
    };
</script>

<TimelineChart
    bind:selectedID
    bind:start_ts
    bind:end_ts
    {loadData}
    on:update={getData}
/>
