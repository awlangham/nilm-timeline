<script>
    import * as d3 from "d3";
    import Legend from "../visuals/Legend.svelte";
    import { yPadding, margin } from "./utilities";
    import { draw, fade } from "svelte/transition";
    import { quadIn, quadOut } from "svelte/easing";

    export let data = { timestamps: [], P: [], Q: [] },
        yMin,
        yMax,
        yAxisLabel,
        off = false,
        showLegend = false;

    const drawDuration = 500;
    const drawDelay = off ? drawDuration : 0;
    const drawEasing = off ? quadOut : quadIn;

    $: x = data["timestamps"];
    $: y1 = data["P"];
    $: y2 = data["Q"];

    const colorScale = d3.scaleOrdinal(["P", "Q"], d3.schemeTableau10);
    const c1 = colorScale("P"),
        c2 = colorScale("Q");

    let xAxis, yAxis;

    const width = window.innerWidth * 0.3,
        height = window.innerHeight * 0.47;

    $: xMin = Math.min(...x);
    $: xMax = Math.max(...x);

    $: xAxisScale = d3.scaleLinear(
        [xMin, xMax],
        [margin.left, width - margin.right],
    );
    $: yAxisScale = d3.scaleLinear(
        [yMin / 1000 - yPadding, yMax / 1000 + yPadding],
        [height - margin.bottom, margin.top],
    );

    $: path1 = d3
        .line()
        .x((d, idx) => xAxisScale(x[idx]))
        .y((d) => yAxisScale(d / 1000));

    $: path2 = d3
        .line()
        .x((d, idx) => xAxisScale(x[idx]))
        .y((d) => yAxisScale(d / 1000));

    $: {
        d3.select(xAxis)
            .call(d3.axisBottom(xAxisScale))
            .style("font-size", "12px");

        d3.select(yAxis)
            .call(d3.axisLeft(yAxisScale))
            .style("font-size", "12px");
    }
</script>

<div class="event-chart-container">
    <svg {width} {height}>
        {#key data}
            <path
                d={path2(y2)}
                fill="none"
                stroke={c2}
                stroke-width="3px"
                in:draw={{ duration: drawDuration, delay: drawDelay, easing: drawEasing}}
            />
            <path
                d={path1(y1)}
                fill="none"
                stroke={c1}
                stroke-width="3px"
                in:draw={{ duration: drawDuration, delay: drawDelay, easing: drawEasing}}
            />
        {/key}

        <g bind:this={yAxis} transform="translate({margin.left}, 0)" />
        <g
            bind:this={xAxis}
            transform="translate(0, {height - margin.bottom})"
        />

        <line
            x1={margin.left}
            y1={margin.top}
            x2={width - margin.right}
            y2={margin.top}
            stroke="black"
        />
        <line
            x1={width - margin.right}
            y1={margin.top}
            x2={width - margin.right}
            y2={height - margin.bottom}
            stroke="black"
        />

        {#each xAxisScale.ticks() as tick}
            <line
                x1={xAxisScale(tick)}
                x2={xAxisScale(tick)}
                y1={margin.top}
                y2={height - margin.bottom}
                fill="none"
                shape-rendering="crispEdges"
                stroke="black"
                stroke-width="1px"
                opacity="0.2"
                in:fade
            />
        {/each}

        {#each yAxisScale.ticks() as tick}
            <line
                x1={margin.left}
                x2={width - margin.right}
                y1={yAxisScale(tick)}
                y2={yAxisScale(tick)}
                fill="none"
                shape-rendering="crispEdges"
                stroke="black"
                stroke-width="1px"
                opacity="0.2"
                in:fade
            />
        {/each}

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

        {#if showLegend}
            <Legend {c1} {c2} x={margin.left + 20} y={margin.top + 20} />
        {/if}
    </svg>
</div>

<style>
    .event-chart-container {
        width: 48%;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 10px;
        border: 2px solid gray;
        border-radius: 10px;
        box-shadow: 3px 1px 4px #888;
        background-color: white;
    }
</style>
