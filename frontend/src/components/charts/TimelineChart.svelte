<script>
    import * as d3 from "d3";
    import { fade } from "svelte/transition";
    import { onMount, createEventDispatcher } from "svelte";
    import RunBar from "../visuals/RunBar.svelte";
    import Title from "../visuals/Title.svelte";

    export let selectedTimestamp,
        start_ts,
        end_ts,
        loadData = [],
        loadNames = [];

    let svgPlot, timeAxis, loadAxis;

    const dispatch = createEventDispatcher();

    const marginTop = 50,
        marginBottom = 75,
        marginLeft = 300,
        marginRight = 50,
        width = window.innerWidth,
        height = window.innerHeight;

    const formatMillisecond = d3.timeFormat(".%L"),
        formatSecond = d3.timeFormat(":%S"),
        formatMinute = d3.timeFormat("%H:%M"),
        formatHour = d3.timeFormat("%H:00"),
        formatDay = d3.timeFormat("%a %d"),
        formatWeek = d3.timeFormat("%b %d"),
        formatMonth = d3.timeFormat("%B"),
        formatYear = d3.timeFormat("%Y");

    const multiFormat = (date) => {
        return (
            d3.timeSecond(date) < date
                ? formatMillisecond
                : d3.timeMinute(date) < date
                  ? formatSecond
                  : d3.timeHour(date) < date
                    ? formatMinute
                    : d3.timeDay(date) < date
                      ? formatHour
                      : d3.timeMonth(date) < date
                        ? d3.timeWeek(date) < date
                            ? formatDay
                            : formatWeek
                        : d3.timeYear(date) < date
                          ? formatMonth
                          : formatYear
        )(date);
    };

    const initialStartTime = start_ts,
        initialEndTime = end_ts;

    let timeAxisScale = d3.scaleTime(
        [initialStartTime, initialEndTime],
        [marginLeft, width - marginRight],
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
        .scaleBand(loadNames, [marginTop, height - marginBottom])
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
                (0.3 * (width - marginLeft - marginRight)) / k,
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
                -(0.3 * (width - marginLeft - marginRight)) / k,
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
                    .tickSize(-(width - marginLeft - marginRight))
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
                x={marginLeft}
                y={marginTop}
                width={width - marginRight - marginLeft}
                height={height - marginBottom - marginTop}
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
                    selectedTimestamp = d.start_ts;
                }}
            />
        {/each}
    </g>

    <g
        bind:this={loadAxisGrid}
        transform="translate({marginLeft}, {-loadAxisScale.step() / 2})"
    ></g>

    <g bind:this={loadAxis} transform="translate({marginLeft}, 0)" out:fade />
    <g
        bind:this={timeAxis}
        transform="translate(0, {height - marginBottom})"
        out:fade
    />
    <line
        x1={marginLeft}
        y1={marginTop}
        x2={width - marginRight}
        y2={marginTop}
        stroke="black"
        out:fade
    />
    <line
        x1={width - marginRight}
        y1={marginTop}
        x2={width - marginRight}
        y2={height - marginBottom}
        stroke="black"
        out:fade
    />

    <Title x="50%" y={marginTop - 10}>
        {startTime.toLocaleString(undefined, { hour12: false })}
        to
        {endTime.toLocaleString(undefined, { hour12: false })}
    </Title>
</svg>

<style>
    #zoomPanButtons {
        padding: 10px;
        position: absolute;
    }

    #zoomPanButtons button {
        font-size: 20px;
    }
</style>
