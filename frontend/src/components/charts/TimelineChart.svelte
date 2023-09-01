<script>
    import * as d3 from "d3";
    import { fade } from "svelte/transition";
    import { onMount, createEventDispatcher } from "svelte";
    import RunBar from "../visuals/RunBar.svelte";
    import Title from "../visuals/Title.svelte";

    export let selectedID,
        start_ts,
        end_ts,
        loadData = [];

    let svgPlot, runBars, timeAxis, loadAxis;

    const dispatch = createEventDispatcher();

    const marginTop = 50,
        marginBottom = 75,
        marginLeft = 270,
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
        [marginLeft, width - marginRight]
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

    $: loadNames = loadData.map((load) => load.name).sort();
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

    $: {
        d3.select(timeAxis)
            .call(d3.axisBottom(timeAxisScale).tickFormat(multiFormat))
            .style("font-size", "24px");
    }

    onMount(() => {
        d3.select(svgPlot).call(zoom);
        dispatch("update");
    });
</script>

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

    <g bind:this={runBars} clip-path="url(#clip-path)">
        {#each loadData as d}
            <RunBar
                start_x={timeAxisScale(d.start_ts / 1000)}
                end_x={timeAxisScale(d.end_ts / 1000)}
                y={loadAxisScale(d.name)}
                fill={colorScale(d.name)}
                height={loadAxisScale.bandwidth()}
                distance={d.distance}
                on:select={() => {
                    selectedID = d.id;
                }}
            />
        {/each}
    </g>

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
