<script>
    import * as d3 from "d3";
    import { onMount, createEventDispatcher } from "svelte";
    import RunBar from "../visuals/RunBar.svelte";
    import Title from "../visuals/Title.svelte";
    import { multiFormat } from "./formatTime";
    import { timelineChartMargin } from "./utilities";

    export let selectedInterval,
        start_ts,
        end_ts,
        loadData = [],
        loadNames = [];

    let svgPlot, timeAxis, loadAxis;

    const dispatch = createEventDispatcher();

    const onKeyPress = (e) => {
        // Allow zooming in/out and translating left/right
        // with arrow keys and WASD
        switch (e.keyCode) {
            case 38:
            case 87:
                zoomIn();
                break;
            case 40:
            case 83:
                zoomOut();
                break;
            case 37:
            case 65:
                translateLeft();
                break;
            case 39:
            case 68:
                translateRight();
                break;
        }
    };

    const width = window.innerWidth,
        height = window.innerHeight,
        initialStartTime = start_ts,
        initialEndTime = end_ts;

    let timeAxisScale = d3.scaleTime(
        [initialStartTime, initialEndTime],
        [timelineChartMargin.left, width - timelineChartMargin.right],
    );
    const origTimeAxisScale = timeAxisScale.copy();

    const zoom = d3.zoom().on("zoom end", (e) => {
        const newtimeAxisScale = e.transform.rescaleX(origTimeAxisScale);
        timeAxisScale.domain(newtimeAxisScale.domain());
        timeAxisScale = timeAxisScale; // Necessary to trigger Svelte reactivity

        if (e.type === "end") {
            // If we are done zooming, refresh the data
            dispatch("update");
        }
    });

    $: loadAxisScale = d3
        .scaleBand(loadNames, [
            timelineChartMargin.top,
            height - timelineChartMargin.bottom,
        ])
        .padding(0.1);
    $: colorScale = d3.scaleOrdinal(loadNames, d3.schemeTableau10);
    $: startTime = timeAxisScale.domain()[0];
    $: endTime = timeAxisScale.domain()[1];

    $: start_ts = startTime.getTime() * 1000;
    $: end_ts = endTime.getTime() * 1000;

    $: d3.select(loadAxis)
        .call(d3.axisLeft(loadAxisScale))
        .style("font-size", "24px");

    $: if (width > 1500) {
        d3.select(timeAxis)
            .call(d3.axisBottom(timeAxisScale).tickFormat(multiFormat)) // Adapt for portrait
            .style("font-size", "24px");
    } else {
        d3.select(timeAxis)
            .call(
                d3
                    .axisBottom(timeAxisScale)
                    .tickFormat(multiFormat)
                    .tickArguments([5]),
            )
            .style("font-size", "24px");
    }

    onMount(() => {
        d3.select(svgPlot).call(zoom);
        dispatch("update");
    });

    const zoomTransitionDuration = 200;

    const zoomIn = () => {
        d3.select(svgPlot)
            .transition()
            .duration(zoomTransitionDuration)
            .call(zoom.scaleBy, 2);
    };

    const zoomOut = () => {
        d3.select(svgPlot)
            .transition()
            .duration(zoomTransitionDuration)
            .call(zoom.scaleBy, 0.5);
    };

    const translateLeft = () => {
        const k = d3.zoomTransform(d3.select(svgPlot).node()).k;
        d3.select(svgPlot)
            .transition()
            .duration(zoomTransitionDuration)
            .call(
                zoom.translateBy,
                (0.3 *
                    (width -
                        timelineChartMargin.left -
                        timelineChartMargin.right)) /
                    k,
                0,
            );
    };

    const translateRight = () => {
        const k = d3.zoomTransform(d3.select(svgPlot).node()).k;
        d3.select(svgPlot)
            .transition()
            .duration(zoomTransitionDuration)
            .call(
                zoom.translateBy,
                -(
                    0.3 *
                    (width -
                        timelineChartMargin.left -
                        timelineChartMargin.right)
                ) / k,
                0,
            );
    };

    const jumpToNow = () => {
        d3.select(svgPlot)
            .transition()
            .duration(zoomTransitionDuration)
            .call(
                zoom.translateTo,
                origTimeAxisScale(new Date().getTime()),
                0,
                [origTimeAxisScale.range()[1], null],
            );
    };

    let interval,
        autoRefresh = false;
    $: if (autoRefresh) {
        interval = setInterval(() => {
            jumpToNow();
        }, 1000);
    } else {
        clearInterval(interval);
    }

    let loadAxisGrid;
    $: {
        d3.select(loadAxisGrid)
            .call(
                d3
                    .axisLeft(loadAxisScale)
                    .tickSize(
                        -(
                            width -
                            timelineChartMargin.left -
                            timelineChartMargin.right
                        ),
                    )
                    .tickFormat("")
                    .tickSizeOuter(0),
            )
            .select("path")
            .style("display", "none");
        d3.select(loadAxisGrid)
            .select(".tick:first-of-type")
            .style("display", "none");
    }
</script>

<div id="zoomPanButtons">
    <button on:click={zoomIn}> Zoom in </button>
    <button on:click={zoomOut}> Zoom out </button>
    <button on:click={translateLeft}> &larr; </button>
    <button on:click={translateRight}> &rarr; </button>
    <input
        type="checkbox"
        id="auto-refresh-checkbox"
        bind:checked={autoRefresh}
    />
    <label for="auto-refresh-checkbox"> Auto Refresh </label>
</div>

<svg id="svgPlot" bind:this={svgPlot} {width} {height}>
    <defs>
        <clipPath id="clip-path">
            <rect
                x={timelineChartMargin.left}
                y={timelineChartMargin.top}
                width={width -
                    timelineChartMargin.right -
                    timelineChartMargin.left}
                height={height -
                    timelineChartMargin.bottom -
                    timelineChartMargin.top}
            />
        </clipPath>
    </defs>

    <g clip-path="url(#clip-path)">
        {#each loadData as d}
            <RunBar
                start_x={timeAxisScale(d.start_ts / 1000)}
                end_x={timeAxisScale(d.end_ts / 1000)}
                y={loadAxisScale(d.name)}
                fill={colorScale(d.name)}
                height={(loadAxisScale.bandwidth() * d.num_on) / d.max_on}
                distance={d.distance}
                on:select={() => {
                    selectedInterval = [d.start_ts, d.end_ts];
                }}
            />
        {/each}
    </g>

    <g
        bind:this={loadAxisGrid}
        transform="translate({timelineChartMargin.left}, {-loadAxisScale.step() /
            2})"
    ></g>

    <g
        bind:this={loadAxis}
        transform="translate({timelineChartMargin.left}, 0)"
    />
    <g
        bind:this={timeAxis}
        transform="translate(0, {height - timelineChartMargin.bottom})"
    />
    <line
        x1={timelineChartMargin.left}
        y1={timelineChartMargin.top}
        x2={width - timelineChartMargin.right}
        y2={timelineChartMargin.top}
        stroke="black"
    />
    <line
        x1={width - timelineChartMargin.right}
        y1={timelineChartMargin.top}
        x2={width - timelineChartMargin.right}
        y2={height - timelineChartMargin.bottom}
        stroke="black"
    />

    <Title x="50%" y={timelineChartMargin.top - 10}>
        {startTime.toLocaleString(undefined, { hour12: false })}
        to
        {endTime.toLocaleString(undefined, { hour12: false })}
    </Title>
</svg>

<svelte:window on:keydown={onKeyPress} />

<style>
    #zoomPanButtons {
        padding: 10px;
        position: absolute;
    }

    #zoomPanButtons button {
        font-size: 20px;
    }
</style>
