<script>
    import * as d3 from "d3";
    import Legend from "../visuals/Legend.svelte";
    import { onMount } from "svelte";
    import { exemplarColor } from "../../constants";
    import { yMinDefault, yMaxDefault, margin } from "./utilities";

    export let x1, y1, c1, x2, y2, yAxisLabel;

    let xAxis, yAxis;

    const width = window.innerWidth * 0.48,
        height = window.innerHeight * 0.8;

    const haveExemplar = x2 && y2;

    let xMin, xMax, yMin, yMax;
    if (haveExemplar) {
        xMin = Math.min(...x1.concat(x2));
        xMax = Math.max(...x1.concat(x2));
        yMin = Math.min(...y1.concat(y2).concat([yMinDefault]));
        yMax = Math.max(...y1.concat(y2).concat([yMaxDefault]));
    } else {
        xMin = Math.min(...x1);
        xMax = Math.max(...x1);
        yMin = Math.min(...y1.concat([yMinDefault]));
        yMax = Math.max(...y1.concat([yMaxDefault]));
    }

    const xAxisScale = d3.scaleLinear(
            [xMin, xMax],
            [margin.left, width - margin.right],
        ),
        yAxisScale = d3.scaleLinear(
            [yMin / 1000, yMax / 1000],
            [height - margin.bottom, margin.top],
        );

    const path = d3
        .line()
        .x((d, idx) => xAxisScale(x1[idx]))
        .y((d) => yAxisScale(d / 1000));

    onMount(() => {
        d3.select(xAxis)
            .call(d3.axisBottom(xAxisScale))
            .style("font-size", "24px");

        d3.select(yAxis)
            .call(d3.axisLeft(yAxisScale))
            .style("font-size", "24px");
    });
</script>

<svg {width} {height}>
    <Legend {c1} {haveExemplar} x={margin.left + 20} y={margin.top + 20} />

    {#if haveExemplar}
        <path
            d={path(y2)}
            fill="none"
            stroke={exemplarColor}
            stroke-width="3px"
        />
    {/if}
    <path d={path(y1)} fill="none" stroke={c1} stroke-width="3px" />

    <g bind:this={yAxis} transform="translate({margin.left}, 0)" />
    <g bind:this={xAxis} transform="translate(0, {height - margin.bottom})" />

    <text
        x="50%"
        y={height - margin.bottom + 60}
        text-anchor="middle"
        font-family="sans-serif"
        font-size="24px"
    >
        Time (s)
    </text>

    <text
        transform="translate(50, {height / 2}),rotate(-90)"
        text-anchor="middle"
        font-family="sans-serif"
        font-size="24px"
    >
        {yAxisLabel}
    </text>
</svg>
