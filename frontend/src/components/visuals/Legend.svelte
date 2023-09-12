<script>
    import { fade } from "svelte/transition";
    import { exemplarColor } from "../../constants.js";

    export let c1, x, y, inConfig;

    const radius = 10;
</script>

<g in:fade={inConfig}>
    <circle cx={x + radius} cy={y + radius} r={radius} fill={c1} />
    <text
        x={x + 2 * radius + 10}
        y={y + 2 * radius}
        dominant-baseline="text-after-edge"
    >
        Selected
    </text>

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
</g>

<style>
    text {
        font-family: sans-serif;
    }
</style>
