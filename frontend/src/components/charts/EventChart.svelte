<script>
    import * as d3 from "d3";
    import Legend from "../visuals/Legend.svelte";
    import { yPadding, eventChartMargin } from "./utilities";
    import { draw, fade } from "svelte/transition";
    import { quadIn, quadOut } from "svelte/easing";

    export let data = { timestamps: [], P: [], Q: [] },
        yMin,
        yMax,
        exemplar = false,
        off = false,
        showLegend = false;

    const c1 = exemplar ? "#aec7e8" : "#1f77b4";
    const c2 = exemplar ? "#ffbb78" : "#ff7f0e";

    const drawDuration = 500;
    const drawDelay = off ? drawDuration : 0;
    const drawEasing = off ? quadOut : quadIn;

    $: x = data["timestamps"];
    $: y1 = data["P"];
    $: y2 = data["Q"];

    let xAxis, yAxis;

    // const width = window.innerWidth * 0.35,
    //     height = window.innerHeight * 0.47;

    let svg, rect, width, height;

    $: if (svg) {
        rect = svg.getBoundingClientRect();
        width = rect.width;
        height = rect.height;
    }

    $: xMin = Math.min(...x);
    $: xMax = Math.max(...x);

    $: xAxisScale = d3.scaleLinear(
        [xMin, xMax],
        [eventChartMargin.left, width - eventChartMargin.right],
    );
    $: yAxisScale = d3.scaleLinear(
        [yMin / 1000 - yPadding, yMax / 1000 + yPadding],
        [height - eventChartMargin.bottom, eventChartMargin.top],
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
    <svg bind:this={svg}>
        <!-- <defs>
            <filter id="shadow">
                <feDropShadow
                    dx="0.2"
                    dy="1.5"
                    flood-opacity="0.5"
                    stdDeviation="1"
                />
            </filter>
        </defs> -->

        {#key data}
            <path
                d={path2(y2)}
                fill="none"
                stroke={c2}
                stroke-width="4px"
                in:draw={{
                    duration: drawDuration,
                    delay: drawDelay,
                    easing: drawEasing,
                }}
            />
            <path
                d={path1(y1)}
                fill="none"
                stroke={c1}
                stroke-width="4px"
                in:draw={{
                    duration: drawDuration,
                    delay: drawDelay,
                    easing: drawEasing,
                }}
            />
        {/key}

        <g
            bind:this={yAxis}
            transform="translate({eventChartMargin.left}, 0)"
        />
        <g
            bind:this={xAxis}
            transform="translate(0, {height - eventChartMargin.bottom})"
        />

        <line
            x1={eventChartMargin.left}
            y1={eventChartMargin.top}
            x2={width - eventChartMargin.right}
            y2={eventChartMargin.top}
            stroke="black"
        />
        <line
            x1={width - eventChartMargin.right}
            y1={eventChartMargin.top}
            x2={width - eventChartMargin.right}
            y2={height - eventChartMargin.bottom}
            stroke="black"
        />

        {#each xAxisScale.ticks() as tick}
            <line
                x1={xAxisScale(tick)}
                x2={xAxisScale(tick)}
                y1={eventChartMargin.top}
                y2={height - eventChartMargin.bottom}
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
                x1={eventChartMargin.left}
                x2={width - eventChartMargin.right}
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
            y={height - eventChartMargin.bottom + 60}
            text-anchor="middle"
            font-family="sans-serif"
            font-size="24px"
        >
            Time (s)
        </text>

        {#if showLegend}
            <Legend
                {c1}
                {c2}
                x={eventChartMargin.left + 20}
                y={eventChartMargin.top + 20}
            />
        {/if}
    </svg>
</div>

<style>
    svg {
        width: 100%;
        height: 100%;
    }
    /* .event-chart-container {
        width: 48%;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 10px;
        border: 2px solid gray;
        border-radius: 10px;
        box-shadow: 3px 1px 4px #888;
        background-color: white;
    } */

    .event-chart-container {
        display: flex;
        flex: 1;
    }
</style>
