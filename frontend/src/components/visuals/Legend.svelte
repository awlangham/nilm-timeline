<script>
    export let c1, c2, x, y;

    const radius = 10;
</script>

<g>
    <rect
        x={x - 5}
        y={y - 5}
        width="100px"
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
        P (kW)
    </text>

    <circle cx={x + radius} cy={y + radius + 40} r={radius} fill={c2} />
    <text
        x={x + 2 * radius + 10}
        y={y + 2 * radius + 40}
        dominant-baseline="text-after-edge"
    >
        Q (kVar)
    </text>
</g>

<style>
    text {
        font-family: sans-serif;
    }
</style>
