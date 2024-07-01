<script>
    import { exemplarColor } from "../../constants.js";

    export let haveExemplar, c1, x, y;

    const radius = 10;
</script>

<g>
    <rect
        x={x - 5}
        y={y - 5}
        width="110px"
        height="70px"
        fill="white"
        stroke="black"
        stroke-width="1px"
        rx="10px"
        ry="10px"
    />
    <circle cx={x + radius} cy={y + radius} r={radius} fill={c1} />
    <text
        x={x + 2 * radius + 10}
        y={y + 2 * radius}
        dominant-baseline="text-after-edge"
    >
        Selected
    </text>

    {#if haveExemplar}
        <circle
            cx={x + radius}
            cy={y + radius + 40}
            r={radius}
            fill={exemplarColor}
        />
        <text
            x={x + 2 * radius + 10}
            y={y + 2 * radius + 40}
            dominant-baseline="text-after-edge"
        >
            Baseline
        </text>
    {/if}
</g>

<style>
    text {
        font-family: sans-serif;
    }
</style>
