<script>
    import * as d3 from "d3";
    import { draw, fade } from "svelte/transition";
    import Legend from "../visuals/Legend.svelte";
    import { onMount } from "svelte";
    import { exemplarColor } from "../../constants";

    export let x1, y1, c1, x2, y2, yAxisLabel;

    let xAxis, yAxis;

    const yMinDefault = -50,
        yMaxDefault = 50;

    const marginTop = 50,
        marginBottom = 75,
        marginLeft = 150,
        marginRight = 50,
        width = window.innerWidth * 0.48,
        height = window.innerHeight * 0.8;

    const inConfig = { delay: 0 },
        drawConfig = { duration: 750, delay: 0 };

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
            [marginLeft, width - marginRight],
        ),
        yAxisScale = d3.scaleLinear(
            [yMin / 1000, yMax / 1000],
            [height - marginBottom, marginTop],
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
    <Legend {c1} {haveExemplar} x={marginLeft + 20} y={marginTop + 20} {inConfig} />

    {#if haveExemplar}
        <path
            d={path(y2)}
            fill="none"
            stroke={exemplarColor}
            stroke-width="3px"
            transition:draw={drawConfig}
        />
    {/if}
    <path
        d={path(y1)}
        fill="none"
        stroke={c1}
        stroke-width="3px"
        transition:draw={drawConfig}
    />

    <g
        bind:this={yAxis}
        transform="translate({marginLeft}, 0)"
        in:fade={inConfig}
    />
    <g
        bind:this={xAxis}
        transform="translate(0, {height - marginBottom})"
        in:fade={inConfig}
    />

    <text
        x="50%"
        y={height - marginBottom + 60}
        text-anchor="middle"
        font-family="sans-serif"
        font-size="24px"
        in:fade={inConfig}
    >
        Time (s)
    </text>

    <text
        transform="translate(50, {height / 2}),rotate(-90)"
        text-anchor="middle"
        font-family="sans-serif"
        font-size="24px"
        in:fade={inConfig}
    >
        {yAxisLabel}
    </text>
</svg>
