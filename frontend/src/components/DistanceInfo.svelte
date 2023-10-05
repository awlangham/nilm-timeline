<script>
    export let distance, numDailyRuns;
</script>

<div>
    <p>Distance: {distance.toFixed(2)}</p>
    <p>Num. runs in previous 24h: {numDailyRuns}</p>
</div>

<style>
    div {
        width: 50%;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
        font-family: sans-serif;
    }
</style>
